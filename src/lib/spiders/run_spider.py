import asyncio

from .infrastructure.occ import OccScraper


async def main():
    urls = [
        "https://www.occ.com.mx/empleos/de-desarrollador-jr/en-ciudad-de-mexico/?tm=7&jobid=20882233",
    ]
    scraper = OccScraper()

    for url in urls:
        scraped_job = await scraper.run(url=url, use_mock=True)
        print(scraped_job, end="\n")


if __name__ == "__main__":
    asyncio.run(main())
