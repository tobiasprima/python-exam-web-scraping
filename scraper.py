import asyncio
from typing import Any
from utils.page_factory import PageFactory
from utils.logger import get_logger
from utils.browser_manager import BrowserManager
from utils.config import Config

class MelbourneScraper:
    """Main orchestrator for scraping."""

    DEFAULT_BASE_URL = "https://www.melbourne.vic.gov.au/planning-permit-register"

    def __init__(self, config: Config)-> None:
        self.config = config
        self.base_url: str = self.DEFAULT_BASE_URL
    
    async def run(self, rows: list[dict[str, Any]])-> None:
        print(f"Processing {len(rows)} rows...")

        async with BrowserManager(headless=self.config.headless) as bm:
            sem = asyncio.Semaphore(self.config.contexts_per_browser)
            async def scrape_row(row: dict[str, Any]) -> None:
                async with sem:  # limit concurrency
                    page = await bm.new_page()
                    try:
                        date_from = row.get("date_from", "")
                        date_to = row.get("date_to", "")
                        
                        case_name = f"{date_from}_to_{date_to}"
                        self.logger = get_logger(self.__class__.__name__, case_name)
                        self.logger.info(f"Scraping row with date_from={date_from}, date_to={date_to}")

                        await page.goto(self.base_url)

                        search_page = PageFactory.get_page(page, "search", case_name)
                        await search_page.search(date_from, date_to)

                        results_page = PageFactory.get_page(page, "results", case_name)
                        urls: list[str] = await results_page.get_results()

                        for url in urls:
                            await page.goto(url)
                            details_page = PageFactory.get_page(page, "details", case_name)
                            data: dict[str, str] = await details_page.scrape_details()
                            self.logger.info(f"Scraped data: {data}")
                    finally:
                        await page.close()
            
            tasks = [scrape_row(row) for row in rows]
            await asyncio.gather(*tasks)

