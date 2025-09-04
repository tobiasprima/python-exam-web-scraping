from .base_page import BasePage

class SearchPage(BasePage):
    """Handles search form input and submission."""

    async def search(self, date_from: str, date_to: str):
        self.logger.info("Searching Data.")