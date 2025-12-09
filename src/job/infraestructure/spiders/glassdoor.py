import asyncio

from job.domain.spider_port import BaseScraper, SpiderPort

JOB_GLASSDOOR_URL = ""


class GlassdoorScraper(BaseScraper, SpiderPort):
    def __init__(self):
        super().__init__()
        self.selectors = {"title": ""}

    def _parse_html_content(self, html_content: str, url: str):
        pass

    async def fetch_and_parse(self, url: str) -> dict:
        pass


async def main():
    glassdoor_scraper = GlassdoorScraper()
    job_data = glassdoor_scraper.fetch_and_parse(JOB_GLASSDOOR_URL)

    if job_data:
        print("\n--- Información de la Vacante ---")
        for [key, value] in job_data.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("No se pudo obtener la información de la vacante.")


if __name__ == "__main__":
    asyncio.run(main())
