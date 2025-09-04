from playwright.async_api import async_playwright, Page, BrowserContext

class BrowserManager:
    """Wrapper for Playwright browser context management."""

    def __init__(self, headless: bool =True)-> None:
        self.headless = headless
        self.browser = None
        self.page = None

    async def __aenter__(self) -> "BrowserManager":
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        return self

    async def __aexit__(self, exc_type, exc, tb)-> None:
        await self.browser.close()
        await self.playwright.stop()
        
    async def new_page(self) -> Page:
        """Open a new isolated context + page."""
        context: BrowserContext = await self.browser.new_context()
        return await context.new_page()

