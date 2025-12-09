import logging
import random

from playwright.async_api import Page
from selectolax.lexbor import LexborHTMLParser

from config.config_service import ConfigService
from job.domain.ports.spider_port import BaseScraper, SpiderPort
from job.infraestructure.strategies.concrete_strategies.close_with_button import (
    CloseWithBotton,
)
from job.infraestructure.strategies.concrete_strategies.close_with_overlay import (
    CloseWithOverlay,
)

logger = logging.getLogger(__name__)


class LinkedinScraper(BaseScraper, SpiderPort):
    def __init__(self):
        super().__init__()
        linkedin_cofing = ConfigService.get_site_config("linkedin")
        self.button_strategy = CloseWithBotton()
        self.overlay_strategy = CloseWithOverlay()
        self.selectors = linkedin_cofing["selectors"]
        # self.selectors = {
        #     "modal_overlay": [".modal__overlay[aria-hidden='false']"],
        #     "modal_content": [
        #         "section[aria-labelledby='base-contextual-sign-in-modal-modal-header']",
        #         "section[aria-modal]",
        #     ],
        #     "modal_dismiss_btn": [
        #         ".modal__dismiss",
        #         "button[aria-label='Dismiss']",
        #         "button[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']",
        #     ],
        #     "main_content": ["#main-content"],
        #     "title": [".top-card-layout__title"],
        #     "company": [
        #         "a[data-tracking-control-name='public_jobs_topcard-org-name']",
        #     ],
        # }

    async def _close_login_modal_action(self, page: Page):
        """Hook para cerrar la modal de LinkedIn si aparece."""
        try:
            await page.wait_for_selector("[aria-hidden='false']", timeout=5000)
            sign_in_modal_locator = page.locator(
                self.selectors["modal_overlay"][0]
            ).first

            await page.screenshot(path="modal_debug.png")

            if not await sign_in_modal_locator.is_visible():
                print("No apareció modal. Continuamos.")
                return

            print("Modal detectada. Intentando cerrarla...")

            strategies = [self.button_strategy, self.overlay_strategy]
            chosen_strategy = random.choices(
                strategies,
                weights=[0.7, 0.3],
            )[0]
            await chosen_strategy.execute(
                page,
                sign_in_modal_locator,
            )
        except Exception as e:
            print("Unexpected error while handling modal: %s", e)

    def _find_node_with_fallback(self, tree, selectors):
        for selector in selectors:
            node = tree.css_first(selector)
            if node:
                return node
        return None

    def _parse_html_content(self, html_content: str, url: str):
        try:
            tree = LexborHTMLParser(html_content)
            job_info = {"url": url, "title": None, "company": None, "description": None}

            main_node = self._find_node_with_fallback(
                tree, self.selectors["main_content"]
            )

            if not main_node:
                print(
                    "No se encontró el contenedor principal. Posible cambio en la estructura o bloqueo."
                )
                return job_info

            title_node = self._find_node_with_fallback(
                main_node, self.selectors["title"]
            )

            if title_node:
                print("recuperando el texto del title")
                title_text = title_node.text(strip=True)
                job_info["title"] = title_text or None

            company_node = self._find_node_with_fallback(
                main_node, self.selectors["company"]
            )

            if company_node:
                print("recuperando el texto del nombre de la empresa")
                company_text = company_node.text(strip=True)
                job_info["company"] = company_text or None

            return job_info

        except Exception:
            pass

    async def fetch_and_parse(self, url: str):
        html_content = await self._run_with_playwright(
            url, pre_scraper_action=[self._close_login_modal_action]
        )
        if html_content:
            return self._parse_html_content(html_content, url)
        return None
