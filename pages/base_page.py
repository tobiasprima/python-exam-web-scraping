import logging
from playwright.async_api import Page
from utils.logger import get_logger

class BasePage:
    """Base class with common Playwright actions."""

    def __init__(self, page: Page, case_name: str):
        self.page = page
        self.logger = get_logger(self.__class__.__name__, case_name)
        
    async def _wait_for_element(self, selector, timeout: int = 10000):
        """Wait for element, with 10000 default timeout"""
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def click_element(self, selector: str):
        await self._wait_for_element(selector)
        self.logger.info(f"Clicking element: {selector}")
        await self.page.click(selector)

    async def input_text(self, selector: str, text: str):
        await self._wait_for_element(selector)
        self.logger.info(f"Inputting text into {selector}: {text}")
        await self.page.fill(selector, text)

    async def wait_for_element(self, selector: str, timeout: int = 5000):
        await self._wait_for_element(selector)
        self.logger.info(f"Waiting for element: {selector}")
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def scroll_page(self, pixels: int = 500):
        self.logger.info(f"Scrolling page by {pixels} pixels")
        await self.page.evaluate(f"window.scrollBy(0, {pixels})")
