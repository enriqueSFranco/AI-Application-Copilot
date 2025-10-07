from job.domain.ports.spider_port import SpiderPort
from job.domain.value_objects.enums import JobBoard

# from job.domain.value_objects.job_url import JobUrl
from job.domain.value_objects.job_url import JobUrl
from job.infraestructure.spiders.linkedin import LinkedinScraper
from job.infraestructure.spiders.occ import OccScraper


class ScraperFactory:
    """
    Factory para crear la instancia de un Scraper
    basado en la URL de entrada.
    """

    @staticmethod
    def create_scraper(url: str) -> SpiderPort:
        job_url = JobUrl(url)
        print(f"URL: {job_url.site_name}")
        if job_url.site_name.startswith(JobBoard.OCC.value):
            print("⚪️ OccScraper runing...")
            return OccScraper()
        elif job_url.site_name.startswith(JobBoard.LINKEDIN.value):
            print("🔵 Linkedin runing...")
            return LinkedinScraper()
        else:
            raise ValueError(f"No hay un scraper disponible para la URL: {url}")
