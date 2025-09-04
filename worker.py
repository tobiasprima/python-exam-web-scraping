import asyncio
from utils.scraper_factory import ScraperFactory

async def run_worker(scraper_type="melbourne"):
    scraper_cls = ScraperFactory.get_scraper(scraper_type)
    melbourne_scraper = scraper_cls()
    await melbourne_scraper.run()
