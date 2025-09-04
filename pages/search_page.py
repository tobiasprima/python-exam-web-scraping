from locators.search_page_locators import SearchPageLocators
from .base_page import BasePage

class SearchPage(BasePage):
    """Handles search form input and submission."""

    async def search(self, date_from: str, date_to: str):
        self.logger.info("Clicking date range tab.")
        await self.click_element(SearchPageLocators.DATE_RANGE_TAB)
        
        self.logger.info("Filling Date Ranges")
        await self.input_text(SearchPageLocators.DATE_FROM, date_from)
        await self.input_text(SearchPageLocators.DATE_TO, date_to)
        
        self.logger.info("Clicking search button.")
        await self.click_element(SearchPageLocators.SEARCH_BUTTON)