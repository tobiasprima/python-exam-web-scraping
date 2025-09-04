import datetime
from typing import Any

from utils.helpers import normalize_key
from .base_page import BasePage

class DetailsPage(BasePage):
    """Scrapes details from a single result page."""

    async def scrape_details(self, details_url: str) -> dict[str, Any]:
        details = {}

        rows = await self.page.query_selector_all("table tr")
        for row in rows:
            key_el = await row.query_selector("th")
            val_el = await row.query_selector("td")
            if key_el and val_el:
                key = (await key_el.inner_text()).strip()
                value = (await val_el.inner_text()).strip()
                if key:
                    key_norm = normalize_key(key)
                    details[key_norm] = value

        # Build final dict
        result: dict[str, Any] = {}
        if "application_number" in details:
            result["id"] = details.pop("application_number")

        result["details_url"] = details_url
        result["date_scraped"] = datetime.datetime.now().isoformat()

        # Add the rest of the normalized fields
        result.update(details)

        return result
