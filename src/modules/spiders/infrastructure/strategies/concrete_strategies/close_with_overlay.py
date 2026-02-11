import asyncio
import random

from playwright.async_api import Locator, Page

from job.infraestructure.strategies.close_modal_strategy import CloseModalStrategy


class CloseWithOverlay(CloseModalStrategy):
    async def execute(self, page: Page, modal_locator: Locator):
        print("[Strategy-Overlay]: Intentando cerrar la modal con un clic en el fondo.")
        try:
            box = await modal_locator.bounding_box()
            if box:
                x = box["x"] + random.uniform(box["width"] * 0.3, box["width"] * 0.7)
                y = box["y"] + random.uniform(box["height"] * 0.3, box["height"] * 0.7)
                print(f"Clicking overlay at ({x:.1f}, {y:.1f})")
                await asyncio.sleep(random.uniform(0.2, 0.5))
                await page.mouse.click(x, y, delay=random.uniform(120, 250))
                await modal_locator.wait_for(state="hidden", timeout=5000)
                print("[Strategy-Overlay]: Modal cerrada con éxito.")
                return True
        except Exception as e:
            print(f"[Strategy-Overlay]: Error al cerrar con el overlay: {e}")
            return False
