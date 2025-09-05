import pytest
from utils.scraper_factory import ScraperFactory
from scraper import MelbourneScraper

def test_scraper_factory_returns_melbourne_scraper():
    scraper_class = ScraperFactory.get_scraper("melbourne")
    assert scraper_class is MelbourneScraper

def test_scraper_factory_invalid_type():
    with pytest.raises(ValueError):
        ScraperFactory.get_scraper("unknown")
