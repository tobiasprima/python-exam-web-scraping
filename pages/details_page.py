from .base_page import BasePage

class DetailsPage(BasePage):
    """Scrapes details from a single result page."""

    async def scrape_details(self):
        self.logger.info("Scraping details from page...")
