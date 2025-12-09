import logging

from selectolax.lexbor import LexborHTMLParser

from job.domain.spider_port import BaseScraper, SpiderPort

logger = logging.getLogger(__name__)


class OccScraper(BaseScraper, SpiderPort):
    def __init__(self):
        super().__init__()
        self.selectors = {
            "container": ["div[data-offers-grid-detail-container]"],
            "title": ["p[data-offers-grid-detail-title]"],
            "company": ["mt-1 line-clamp-1"],
        }

    def _find_node_with_fallback(self, tree, selectors):
        for selector in selectors:
            node = tree.css_first(selector)
            if node:
                return node
        return None

    def _parse_html_content(self, html_content: str, url: str):
        try:
            tree = LexborHTMLParser(html_content)
            job_info = {"url": url, "title": None, "company": None, "description": None}

            container = self._find_node_with_fallback(tree, self.selectors["container"])

            if not container:
                print(
                    "No se encontró el contenedor principal. Posible cambio en la estructura o bloqueo."
                )
                return job_info

            title_node = self._find_node_with_fallback(
                container, self.selectors["title"]
            )
            if title_node:
                title_text = title_node.text(strip=True)

                job_info["title"] = title_text or None

            company_node = self._find_node_with_fallback(
                container, self.selectors["company"]
            )
            if company_node:
                company_text = company_node.text(deep=False, strip=True)
                job_info["company"] = company_text if company_text else None

            return job_info
        except Exception as e:
            print(f"Error al parsear el HTML: {e}")
            return None

    async def fetch_and_parse(self, url: str):
        html_content = await self._run_with_playwright(url)
        if html_content:
            return self._parse_html_content(html_content, url)
        return None
