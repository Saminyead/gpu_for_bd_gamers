import pytest
from gpu4bdgamers.scraping_attributes import (
    ScrapingAttributes, NoUrlTagStrOrCssSelError
)

@pytest.fixture
def scraping_attributes_no_tagstr_csssel() -> ScrapingAttributes:
    return ScrapingAttributes(
        first_page_url = "http://someurl.com",
        card_css_sel = "some_card_css_sel",
        gpu_name_css_sel = "some_gpu_name_css_sel",
        gpu_price_css_sel = "some_price_sel",
        retailer_name = "Some Retailer Inc."
    )

def test_get_pages_no_url_tag_or_css_sel(
    scraping_attributes_no_tagstr_csssel: ScrapingAttributes
) -> None:
    """Test to check if error is raised when both next_page_url_tag_str and
    next_page_url_css_sel are None"""
    with pytest.raises(NoUrlTagStrOrCssSelError):
        scraping_attributes_no_tagstr_csssel.get_pages()
