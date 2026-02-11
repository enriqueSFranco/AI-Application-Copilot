from abc import ABC, abstractmethod

from playwright.async_api import Locator, Page


class CloseModalStrategy(ABC):
    @abstractmethod
    async def execute(self, page: Page, modal_locator: Locator):
        """Ejecuta la estrategia para cerrar la modal

        Args:
            modal_locator (Locator): Localizador del contenedor de la modal
            page (Page): El objeto Page de Playwright
        """
        pass
