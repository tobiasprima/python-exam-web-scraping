from playwright.async_api import async_playwright
from utils.page_factory import PageFactory
from utils.logger import get_logger
from utils.config import load_config

class MelbourneScraper:
    """Main orchestrator for scraping."""

    def __init__(self, config_path="config.json"):
        self.config = load_config(config_path)
        self.logger = get_logger(self.__class__.__name__)

    async def run(self):
        self.logger.info("Starting MelbourneScraper...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            search_page = PageFactory.get_page(page, "search")
            results_page = PageFactory.get_page(page, "results")
            details_page = PageFactory.get_page(page, "details")

            await browser.close()
