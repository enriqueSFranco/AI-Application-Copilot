import logging
from typing import List, Optional

from selectolax.lexbor import LexborHTMLParser, LexborNode

from config.config_service import ConfigService
from job.domain.job_entity import Job
from job.domain.ports.spider_port import BaseScraper, SpiderPort

logger = logging.getLogger(__name__)


class OccScraper(BaseScraper, SpiderPort):
    """Scraper de OCC con soporte para recuperar titulo, empresa y descripción."""

    def __init__(self):
        super().__init__()
        occ_config = ConfigService.get_site_config("occ")
        self.selectors = occ_config["selectors"]
        logger.debug(f"Selectores cargados: {self.selectors}")

    def _find_node_with_fallback(
        self, tree: LexborHTMLParser | None, selectors: List[str]
    ) -> Optional[LexborHTMLParser]:
        for selector in selectors:
            node = tree.css_first(selector)
            if node:
                return node
        return None

    def _parse_html_safely(self, html_content: str) -> LexborHTMLParser:
        try:
            clean_html = html_content.encode("utf-8", "ignore").decode(
                "utf-8", "ignore"
            )
            return LexborHTMLParser(clean_html)
        except Exception as e:
            print(f"[DEBUG] Error al parsear HTML: {e}")
            # Path("debug_failed_html.html").write_text(html_content, encoding="utf-8")
            raise

    def _extract_text_safely(
        self, node: Optional[LexborNode], default_value: str, deep: bool = True
    ) -> str:
        if not node:
            logger.warning(
                f"Nodo no encontrado. Usando valor por defecto: '{default_value}'"
            )
            return default_value

        if deep:
            text = node.text(strip=True)
        else:
            text = node.text(deep=False, strip=True)

        return " ".join(text.split()) if text else default_value

    def _parse_html_content(self, html_content: str, url: str) -> Optional[Job]:
        """
        Analiza el HTML del contenedor y extrae la información de la vacante
        """
        try:
            tree = self._parse_html_safely(html_content)

            job_card_detail_container = self._find_node_with_fallback(
                tree, self.selectors["job_card_detail"]
            )

            if not job_card_detail_container:
                print("no se encontro el job detail container")
                return

            container = self._find_node_with_fallback(tree, self.selectors["container"])

            if not container:
                print(
                    "No se encontró el contenedor principal. Posible cambio en la estructura o bloqueo."
                )
                return Job.create(
                    url,
                    title="Sin titulo",
                    company="Sin empresa",
                    description="",
                    category="",
                )

            title_node = self._find_node_with_fallback(
                container, self.selectors["title"]
            )
            title_text = title_node.text(strip=True) if title_node else "Sin titulo"

            if not title_node:
                print("no ha title_node")

            company_node = self._find_node_with_fallback(
                container, self.selectors["company"]
            )

            if not company_node:
                print("no hay company_node")

            description_node = self._find_node_with_fallback(
                container, self.selectors["description_container"]
            )

            description_content_node = self._find_node_with_fallback(
                description_node, self.selectors["description"]
            )

            description_text = (
                description_content_node.text(strip=True)
                if description_content_node
                else ""
            )

            raw_company_text = (
                company_node.text(deep=False, strip=True)
                if company_node
                else "Empresa confidencial"
            )

            company_text = " ".join(raw_company_text.split())

            job_info = Job.create(
                url=url,
                title=title_text,
                company=company_text,
                description=description_text,
                category="",
            )

            return job_info
        except Exception as e:
            print(f"Error al parsear el HTML: {e}")
            return None

    async def fetch_and_parse(self, url: str):
        html_content = await self._run_with_playwright(url)
        if html_content:
            return self._parse_html_content(html_content, url)
        return Job.create(
            url=url,
            title="Sin título",
            company="Sin empresa",
            description="",
            category="",
        )
