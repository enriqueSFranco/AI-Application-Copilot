from playwright.async_api import Browser, async_playwright


class BrowserManager:
    _instance = None

    def __init__(self):
        self.playwright = None
        self._browser: Browser | None = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = BrowserManager()
            await cls._instance._init_browser()

        return cls._instance

    async def _init_browser(self):
        if self.playwright is None or self._browser is None:
            self.playwright = await async_playwright().start()
            self._browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-gpu",
                    "--no-sandbox",
                ],
            )
        return self._browser

    async def new_context(
        self, user_agent: str | None = None, extra_http_headers: dict | None = None
    ):
        if not self._browser:
            await self._init_browser()
        context_args = {}
        if user_agent:
            context_args["user_agent"] = user_agent
        if extra_http_headers:
            context_args["extra_http_headers"] = extra_http_headers

        # Evitar cargar imágenes y recursos pesados para acelerar scraping
        context_args["bypass_csp"] = True
        context_args["java_script_enabled"] = True
        return await self._browser.new_context(
            **context_args,
            viewport={"width": 425, "height": 532},
            is_mobile=False,
            has_touch=False,
        )

    @staticmethod
    async def close_browser(self):
        if self._browser:
            await self._browser.close()
        if self.playwright:
            self.playwright = None

        BrowserManager._instance = None

    @property
    def browser(self):
        return self._browser
