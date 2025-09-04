import asyncio
from typing import Any
from utils.page_factory import PageFactory
from utils.logger import get_logger
from utils.browser_manager import BrowserManager
from utils.config import Config
from utils.results_writer import save_results

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
                        unique_id = row.get("id")
                        
                        case_name = f"{date_from}_to_{date_to}"
                        self.logger = get_logger(self.__class__.__name__, case_name)
                        self.logger.info(f"Scraping row with date_from={date_from}, date_to={date_to}")

                        await page.goto(self.base_url)

                        search_page = PageFactory.get_page(page, "search", case_name)
                        await search_page.search(date_from, date_to)

                        results_page = PageFactory.get_page(page, "results", case_name)
                        results = await results_page.get_results("https://www.melbourne.vic.gov.au")
                        
                        save_results(results, self.config.output_dir, case_name, "results", unique_id)
                        
                        details = []
                        details_sem = asyncio.Semaphore(self.config.details_concurrency)
                        
                        async def scrape_detail(r: dict[str, Any]):
                            async with details_sem:
                                detail_page = await bm.new_page()
                                try:
                                    await detail_page.goto(r["url"])
                                    dp = PageFactory.get_page(detail_page, "details", case_name)
                                    detail_data = await dp.scrape_details(r["url"])
                                    details.append(detail_data)
                                finally:
                                    await detail_page.close()

                        await asyncio.gather(*(scrape_detail(r) for r in results))

                        save_results(details, self.config.output_dir, case_name, "details", unique_id)

                    finally:
                        await page.close()
            
            tasks = [scrape_row(row) for row in rows]
            await asyncio.gather(*tasks)