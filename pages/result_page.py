import datetime
from typing import Any

from locators.result_page_locators import ResultPageLocators
from .base_page import BasePage

class ResultsPage(BasePage):
    """Handles results listing and pagination."""

    async def get_results(self, base_url: str) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        while True:
            # Extract all rows from current page
            rows = await self.page.query_selector_all(ResultPageLocators.TABLE_ROWS)
            for row in rows:
                link = await row.query_selector(ResultPageLocators.APPLICATION_LINK)
                if link:
                    id_text = (await link.inner_text()).strip()
                    href = await link.get_attribute("href")
                    full_url = f"{base_url}{href}" if href else None
                    results.append({
                        "id": id_text,
                        "url": full_url,
                        "date_collected": datetime.datetime.now().isoformat()
                    })

            # Check if Next button exists
            next_button = await self.page.query_selector(ResultPageLocators.NEXT_BUTTON)
            if next_button:
                await next_button.click()
                await self.page.wait_for_selector(ResultPageLocators.TABLE_ROWS)
            else:
                break

        return results