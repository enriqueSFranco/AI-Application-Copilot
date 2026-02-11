# ScrapeService (orchestrator)


from datetime import datetime

from ..application.dto import ScrapedVacancyDTO
from ..infrastructure.spider_registry import SpiderRegistry


class ScraperService:
    async def scrape_url(self, url: str) -> ScrapedVacancyDTO:
        scraper = SpiderRegistry.get_scraper_for_url(str(url))
        result = await scraper.fetch_and_parse(str(url))

        if not result:
            raise RuntimeError("Scraper failed or blocked")
        dto = ScrapedVacancyDTO(**result, scraped_at=datetime.now())

        # Encola ETL en background
        # etl_process_scraped_vacancy.delay(dto.model_dump())

        return dto
