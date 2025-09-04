from .base_page import BasePage

class ResultsPage(BasePage):
    """Handles results listing."""

    async def get_results(self) -> list[str]:
        self.logger.info("Collecting result links...")
