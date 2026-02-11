import asyncio

from .infrastructure.occ import OccScraper


async def main():
    urls = [
        "url_de_la_vacante",
    ]
    scraper = OccScraper()

    for url in urls:
        scraped_job = await scraper.run(url=url, use_mock=True)
        print(scraped_job, end="\n")


if __name__ == "__main__":
    asyncio.run(main())
