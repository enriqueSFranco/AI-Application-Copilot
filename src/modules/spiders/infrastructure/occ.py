import logging
from pathlib import Path
from typing import Optional

from selectolax.lexbor import LexborHTMLParser

from src.modules.vacancies.domain.value_objects.enums import JobBoard

from ..infrastructure.base_scraper import BaseScraper, SpiderPort

logger = logging.getLogger(__name__)


class OccScraper(BaseScraper, SpiderPort):
    """Scraper específico para OCC Mundial."""

    FIXTURE_PATH = Path("tests/fixtures/occ_sample.html")
    SELECTORS = {
        "container": [
            "div[data-offers-grid-detail-container]",
            "div[data-offers-grid-detail-popup-scroll]",
        ],
        "title": ["p[data-offers-grid-detail-title]", "p.font-h4-m"],
        "company": ["span.line-clamp-2"],
        "location": ["label.font-light"],
        "description": ["div.break-words"],
        "salary": ["p.font-small-strong", "p.font-small-strong span.icon.i_money"],
        "contract_type": [""],
        "posted_date": [""],
    }

    def __init__(self):
        super().__init__()

    def _find_node_with_fallback(self, tree, selectors):
        for selector in selectors:
            node = tree.css_first(selector)
            if node:
                return node
        return None

    def _extract_text(
        self,
        tree: LexborHTMLParser,
        selector_key: str,
        clean: bool = False,
        strip: bool = True,
    ):
        """Busca un nodo, extrae su texto y aplica limpieza opcional."""
        selectors = self.SELECTORS.get(selector_key, [])
        node = self._find_node_with_fallback(tree, selectors)

        if node:
            text = node.text(deep=True, strip=strip)
            return text

        return None

    def extract_by_label(self, label: str):
        pass

    def _parse_html_content(self, html_content: str, url: str):
        """Analiza el contenido HTML y extrae los datos de la vacante."""
        out = {
            "source_url": url,
            "source_type": JobBoard.OCC,
            "title": None,
            "company": None,
            "location": None,
            "description": None,
            "raw_html": html_content,
            "salary": None,
            "skills": [],
            "seniority": None,
            "job_type": None,
            "contract_type": None,
            "posted_date": None,
            "extra": {},
        }

        try:
            tree = LexborHTMLParser(html_content)

            container = self._find_node_with_fallback(tree, self.SELECTORS["container"])

            if not container:
                print(
                    "No se encontró el contenedor principal. Posible cambio en la estructura o bloqueo."
                )
                return out

            out["title"] = self._extract_text(container, "title")

            out["company"] = self._extract_text(container, "company")

            out["location"] = self._extract_text(container, "location")

            out["description"] = self._extract_text(container, "description")

            out["salary"] = self._extract_text(container, "salary")

            print("Vacante:", out)

            return out
        except Exception as e:
            print(f"Error al parsear el HTML: {e}")
            return None

    async def fetch_and_parse(self, url: str):
        html_content = await self._run_with_playwright(url)
        if html_content:
            self.FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
            self.FIXTURE_PATH.write_text(html_content, encoding="utf-8")
            print(f"[OK] HTML guardado en: {self.FIXTURE_PATH}")

            return self._parse_html_content(html_content, url)
        return None

    def _parse_from_file(
        self, filepath: Optional[str] = None, url: str = "https://mock.test"
    ):
        path = Path(filepath) if filepath else self.FIXTURE_PATH

        if not path.exists():
            print(f"[ERROR] Fixture no encontrado en {path}")
            return None

        html = path.read_text(encoding="utf-8")
        return self._parse_html_content(html, url)

    async def run(self, url: str, use_mock=False):
        """
        Ejecuta el scraper en modo real o mock.

        - use_mock=True  → Lee fixture local
        - use_mock=False → Ejecuta Playwright y guarda fixture
        """

        if use_mock:
            print("[MOCK] Usando HTML local…")
            return self._parse_from_file(url=url)

        print("[REAL] Obteniendo HTML real…")
        return await self.fetch_and_parse(url)
