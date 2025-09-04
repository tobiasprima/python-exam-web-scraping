import asyncio
from typing import Any
from utils.file_manager import FileManager
from utils.page_factory import PageFactory
from utils.logger import get_logger
from utils.browser_manager import BrowserManager
from utils.config import Config
from utils.results_writer import ResultsWriter

class MelbourneScraper:
    """Main orchestrator for scraping."""

    DEFAULT_BASE_URL = "https://www.melbourne.vic.gov.au/planning-permit-register"

    def __init__(self, config: Config)-> None:
        self.config = config
        self.base_url: str = self.DEFAULT_BASE_URL
    
    async def run(self, rows: list[dict[str, Any]]) -> None:
        print(f"Processing {len(rows)} rows...")

        async with BrowserManager(headless=self.config.headless) as bm:
            sem = asyncio.Semaphore(self.config.contexts_per_browser)
            tasks = [self._scrape_row(row, bm, sem) for row in rows]
            await asyncio.gather(*tasks)

    async def _scrape_row(self, row: dict[str, Any], bm: BrowserManager, sem: asyncio.Semaphore) -> None:
        async with sem:
            page = await bm.new_page()
            try:
                date_from = row.get("date_from", "")
                date_to = row.get("date_to", "")
                unique_id = row.get("id")
                case_name = f"{date_from}_to_{date_to}"

                logger = get_logger(self.__class__.__name__, case_name)
                logger.info(f"Scraping row with date_from={date_from}, date_to={date_to}")

                await page.goto(self.base_url)
                await PageFactory.get_page(page, "search", case_name).search(date_from, date_to)

                results_page = PageFactory.get_page(page, "results", case_name)
                results = await results_page.get_results("https://www.melbourne.vic.gov.au")

                fm = FileManager(self.config.output_dir, case_name, unique_id)
                writer = ResultsWriter(fm)
                writer.save_all(results, "results")

                details = await self._scrape_details(bm, results, case_name)
                writer.save_all(details, "details")

            finally:
                await page.close()

    async def _scrape_details(self, bm: BrowserManager, results: list[dict[str, Any]], case_name: str) -> list[dict[str, Any]]:
        details = []
        sem = asyncio.Semaphore(self.config.details_concurrency)

        async def scrape_detail(r: dict[str, Any]):
            async with sem:
                page = await bm.new_page()
                try:
                    await page.goto(r["url"])
                    dp = PageFactory.get_page(page, "details", case_name)
                    details.append(await dp.scrape_details(r["url"]))
                finally:
                    await page.close()

        await asyncio.gather(*(scrape_detail(r) for r in results))
        return details