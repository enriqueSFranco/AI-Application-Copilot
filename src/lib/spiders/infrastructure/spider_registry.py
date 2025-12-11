# Registrar scrapers por dominio / source_type


from typing import Dict, Type
from urllib.parse import urlparse

from src.lib.spiders.infrastructure.base_scraper import SpiderPort
from src.lib.spiders.infrastructure.occ import OccScraper


class SpiderRegistry:
    _map: Dict[str, Type[SpiderPort]] = {"occ.com.mx": OccScraper, "occ.mx": OccScraper}

    @staticmethod
    def get_scraper_for_url(url: str) -> SpiderPort:
        hostname = urlparse(url).hostname or ""

        for domain, scraper_cls in SpiderRegistry._map.items():
            if hostname.endswith(domain):
                return scraper_cls()

        raise ValueError(f"No scraper registered for host: {hostname}")
