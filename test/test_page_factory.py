import pytest
from utils.page_factory import PageFactory
from pages.search_page import SearchPage
from pages.result_page import ResultsPage
from pages.details_page import DetailsPage

class DummyPage:
    pass

@pytest.mark.parametrize("page_type,expected_class", [
    ("search", SearchPage),
    ("results", ResultsPage),
    ("details", DetailsPage),
])
def test_page_factory_returns_correct_class(page_type, expected_class):
    dummy = DummyPage()
    obj = PageFactory.get_page(dummy, page_type, "case")
    assert isinstance(obj, expected_class)

def test_page_factory_invalid_type():
    dummy = DummyPage()
    with pytest.raises(ValueError):
        PageFactory.get_page(dummy, "invalid", "case")
