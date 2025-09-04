import asyncio
from typing import Any
from utils.scraper_factory import ScraperFactory
from utils.config import Config

def run_worker(rows: list[dict[str, Any]], config: Config, scraper_type: str = "melbourne") -> None:
    """Sync entrypoint for a worker process."""
    asyncio.run(_run_async(rows, config, scraper_type))

async def _run_async(rows: list[dict[str, Any]], config: Config, scraper_type: str) -> None:
    scraper_cls = ScraperFactory.get_scraper(scraper_type)
    scraper = scraper_cls(config)
    await scraper.run(rows)
