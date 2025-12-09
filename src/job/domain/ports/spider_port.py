import asyncio
import logging
import random
from typing import Callable, Coroutine, List, Optional, Protocol

import playwright
from playwright.async_api import Page

from job.infraestructure.playwright.browser_manager import BrowserManager
from job.infraestructure.utils.user_agent_provider import UserAgentProvider

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class SpiderPort(Protocol):
    """Interfaz (Puerto de entrada) para la lógica de scraping."""

    async def fetch_and_parse(self, url: str) -> dict:
        """
        Obtiene y analiza el contenido de una URL.
        Retorna un diccionario con los datos de la vacante.
        """
        pass


class BaseScraper(Protocol):
    MAX_RETRIES = 3
    RETRY_BACKOFF = (1, 4)  # segundos min y max de espera aleatoria entre reintentos

    def __init__(self):
        self.ua_provider = UserAgentProvider(strategy="random")

    async def _run_with_playwright(
        self,
        url: str,
        pre_scraper_action: Optional[List[Callable[[Page], Coroutine]]] = None,
    ):
        bm = await BrowserManager.get_instance()
        attempt = 0
        while attempt <= self.MAX_RETRIES:
            print(f"[Intento {attempt + 1}/{self.MAX_RETRIES}] Navegando a: {url}")
            user_agent = self.ua_provider.get()
            print(f"User-Agent usado: {user_agent}")

            try:
                context = await bm.new_context(
                    user_agent=user_agent,
                    extra_http_headers={
                        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Upgrade-Insecure-Requests": "1",
                        "Referer": "https://www.google.com",
                    },
                )
                page = await context.new_page()

                async def block_resources(route):
                    bloked_types = ["image", "stylesheet", "font", "media", "websocket"]
                    if route.request.resource_type in bloked_types:
                        await route.abort()
                    else:
                        await route.continue_()

                await page.route("**/*", block_resources)

                await page.goto(url, wait_until="domcontentloaded", timeout=8000)

                for action in pre_scraper_action or []:
                    await action(page)

                html_content = await page.content()

                size = len(html_content)
                if size < 500:
                    raise ValueError(
                        "HTML demasiado pequeño (posible error o bloqueo)."
                    )

                return html_content
            except (playwright.errors.TimeoutError, ValueError) as e:
                logger.warning(f"Error en intento {attempt + 1}: {e}")
                attempt += 1
                if attempt < self.MAX_RETRIES:
                    sleep_time = random.uniform(*self.RETRY_BACKOFF)
                    logger.info(f"Reintentando en {sleep_time:.1f}s...")
                    await asyncio.sleep(sleep_time)
                else:
                    logger.error(f"Fallaron todos los intentos para: {url}")
                    return None
            finally:
                await context.close()

    async def _parse_html_content(self, html_content: str, url: str):
        """Método que cada scraper debe implementar para extraer datos."""
        ...
