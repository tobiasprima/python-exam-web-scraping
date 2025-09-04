from playwright.async_api import async_playwright

class BrowserManager:
    """Wrapper for Playwright browser context management."""

    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        return self.page

    async def __aexit__(self, exc_type, exc, tb):
        await self.browser.close()
        await self.playwright.stop()
