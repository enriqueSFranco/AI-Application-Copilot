# ScrapeService (orchestrator)


import logging
from datetime import datetime

from ..application.dto import ScrapedVacancyDTO
from ..infrastructure.spider_registry import SpiderRegistry


class ScraperService:
    def __init__(self):
        self.logger = logging.getLogger("scraper.service")

    async def scrape_url(self, url: str) -> ScrapedVacancyDTO:
        """
        Método principal que ejecuta el scraping.
        Se ejecuta en background por el endpoint.

        """
        self.logger.info(f"[SCRAPER] Iniciando scraping para URL: {url}")

        scraper = SpiderRegistry.get_scraper_for_url(str(url))
        self.logger.info(
            f"[SCRAPER] Scraper seleccionado: {scraper.__class__.__name__}"
        )

        result = await scraper.fetch_and_parse(str(url))

        if not result:
            self.logger.error(
                "[SCRAPER] Scraper falló o el sitio bloqueó la extracción"
            )
            raise RuntimeError("Scraper failed or blocked")
        dto = ScrapedVacancyDTO(**result, scraped_at=datetime.now())

        # Encola ETL en background
        # etl_process_scraped_vacancy.delay(dto.model_dump())
        self.logger.info(f"[SCRAPER] Scraping finalizado para URL: {url}")
        return dto
