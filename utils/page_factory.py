from pages.search_page import SearchPage
from pages.result_page import ResultsPage
from pages.details_page import DetailsPage

class PageFactory:
    """Factory to return the correct page object."""

    @staticmethod
    def get_page(page, page_type: str):
        if page_type == "search":
            return SearchPage(page)
        if page_type == "results":
            return ResultsPage(page)
        if page_type == "details":
            return DetailsPage(page)
        raise ValueError(f"Unknown page type: {page_type}")
