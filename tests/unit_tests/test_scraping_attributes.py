import pytest
from gpu4bdgamers.scraping import (
    get_page_soup_list,
    get_card_list,
    ElementDoesNotExistError,
    GpuListingAttrs,
    get_price_int_regex
)

from bs4 import BeautifulSoup, Tag


def test_no_next_page_url_element_does_not_exist_error(
    mock_server, no_next_page_url: str
):
    with pytest.raises(ElementDoesNotExistError):
        get_page_soup_list(no_next_page_url, "a")


def test_no_card_element_does_not_exist_error(
    missing_card_soup_list: list[BeautifulSoup],
):
    with pytest.raises(ElementDoesNotExistError):
        get_card_list(missing_card_soup_list, "section > div.card")


def test_gpu_name_price_retail_url_missing_does_not_exist_error(
        missing_gpu_name_in_card: list[Tag],
        missing_gpu_price_in_card: list[Tag],
        missing_retail_url_in_card: list[Tag]
):
    gpu_list_attrs_test = GpuListingAttrs(
        gpu_name_css_sel = "li.gpu-name", 
        gpu_price_css_sel = "li.gpu-price",
        retail_url_css_sel = "li.product-url > a"
    )
    with pytest.raises(ElementDoesNotExistError):
        gpu_list_attrs_test.get_gpu_listing_data(missing_gpu_name_in_card)
        gpu_list_attrs_test.get_gpu_listing_data(missing_gpu_price_in_card)
        gpu_list_attrs_test.get_gpu_listing_data(missing_retail_url_in_card)

def test_get_price_int_regex():
    assert get_price_int_regex("28,000") == 28000
    assert get_price_int_regex("69000") == 69000
    assert get_price_int_regex("BDT. 50,000") == 50000
    assert get_price_int_regex("BDT100,000") == 100000
