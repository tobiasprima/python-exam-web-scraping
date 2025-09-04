from scraper import MelbourneScraper

class ScraperFactory:
    """Factory for selecting the right scraper implementation."""

    @staticmethod
    def get_scraper(scraper_type: str):
        if scraper_type == "melbourne":
            return MelbourneScraper
        raise ValueError(f"Unknown scraper type: {scraper_type}")