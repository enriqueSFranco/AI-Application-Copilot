from abc import ABC, abstractmethod
import string
from playwright.async_api import async_playwright

from job.config.user_agent_provider import UserAgentProvider



class ScraperPort(ABC):
    """Interfaz (Puerto de entrada) para la lógica de scraping."""
    @abstractmethod
    async def fetch_and_parse(self, url: str) -> dict:
        """
        Obtiene y analiza el contenido de una URL.
        Retorna un diccionario con los datos de la vacante.
        """
        pass


class BaseScraper(ABC):
    def __init__(self):
        self.ua_provider = UserAgentProvider(strategy="random")
    
    async def _run_with_playwright(self, url: string):
        user_agent = self.ua_provider.get()
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True, slow_mo=50)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            try:
                print("navegando a la ruta:", url)
                await page.goto(url)
                print("Página cargada. Obteniendo el contenido HTML.")
                html_content = await page.content()
                return html_content
            finally:
                await browser.close()
                await context.close()
    
    @abstractmethod
    async def _parse_html_content(self, html_content: str, url: str):
        """Método que cada scraper debe implementar para extraer datos."""
        pass
