import asyncio
import random

from job.infraestructure.strategies.close_modal_strategy import CloseModalStrategy


class CloseWithBotton(CloseModalStrategy):
    async def execute(self, page, modal_locator):
        print("[Strategy-Button]: Intentando cerrar la modal con un clic en el botón.")
        try:
            dismiss_btn_locator = modal_locator.locator(
                self.selectors["modal_dismiss_btn"][0]
            ).first

            if await dismiss_btn_locator.is_visible():
                await dismiss_btn_locator.hover()
                await asyncio.sleep(random.uniform(0.2, 0.6))
                await dismiss_btn_locator.click(delay=random.uniform(100, 300))
                await modal_locator.wait_for(state="hidden")
                print("[Strategy-Button]: Modal cerrada con éxito.")
                return True
        except Exception:
            print("[Strategy-Button]: Error al cerrar con el botón: {e}")
            return False
