import pytest
from gpu4bdgamers.scraping import (
    get_page_soup_list,
    get_card_list,
    ElementDoesNotExistError,
    GpuListingAttrs,
    GpuListingData,
    get_price_int_regex,
)

from bs4 import BeautifulSoup, Tag
import pydantic


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


def test_get_gpu_listing_data(no_missing_in_card: list[Tag]):
    gpu_list_attrs_test = GpuListingAttrs(
        gpu_name_css_sel="li.gpu-name",
        gpu_price_css_sel="li.gpu-price",
        retail_url_css_sel="li.product-url > a",
        retailer_name="Jerry's Hardware",
    )
    gpu_listing_data = gpu_list_attrs_test.get_gpu_listing_data(no_missing_in_card)
    assert gpu_listing_data == [
        GpuListingData(
            gpu_name="Asus ROG Geforce RTX 3080",
            gpu_price=86000,
            retail_url=pydantic.AnyUrl("https://goslinghardware.com/product/3361"),
            retailer_name="Jerry's Hardware",
        ),
        GpuListingData(
            gpu_name="MSI Radeon RX 6700 XT",
            gpu_price=68000,
            retail_url=pydantic.AnyUrl("https://jerryshardware.com/product/3690"),
            retailer_name="Jerry's Hardware",
        ),
        GpuListingData(
            gpu_name="Zotac Geforce RTX 4060",
            gpu_price=48000,
            retail_url=pydantic.AnyUrl("https://powerpc.com/product/3301"),
            retailer_name="Jerry's Hardware",
        ),
    ]


def test_get_gpu_listing_data_one_missing(
    missing_gpu_name_in_card: list[Tag],
    missing_gpu_price_in_card: list[Tag],
    missing_retail_url_in_card: list[Tag],
):
    gpu_list_attrs_test = GpuListingAttrs(
        gpu_name_css_sel="li.gpu-name",
        gpu_price_css_sel="li.gpu-price",
        retail_url_css_sel="li.product-url > a",
        retailer_name="Jerry's Hardware",
    )
    gpu_listing_data_no_name = gpu_list_attrs_test.get_gpu_listing_data(
        missing_gpu_name_in_card
    )
    gpu_listing_data_no_price = gpu_list_attrs_test.get_gpu_listing_data(
        missing_gpu_price_in_card
    )
    gpu_listing_data_no_retail_url = gpu_list_attrs_test.get_gpu_listing_data(
        missing_retail_url_in_card
    )
    assert gpu_listing_data_no_name == [
        GpuListingData(
            gpu_name="Asus ROG Geforce RTX 3080",
            gpu_price=86000,
            retail_url=pydantic.AnyUrl("https://goslinghardware.com/product/3361"),
            retailer_name="Jerry's Hardware",
        ),
        GpuListingData(
            gpu_name="Zotac Geforce RTX 4060",
            gpu_price=48000,
            retail_url=pydantic.AnyUrl("https://powerpc.com/product/3301"),
            retailer_name="Jerry's Hardware",
        ),
    ]
    assert gpu_listing_data_no_price == [
        GpuListingData(
            gpu_name="Asus ROG Geforce RTX 3080",
            gpu_price=86000,
            retail_url=pydantic.AnyUrl("https://goslinghardware.com/product/3361"),
            retailer_name="Jerry's Hardware",
        ),
        GpuListingData(
            gpu_name="MSI Radeon RX 6700 XT",
            gpu_price=68000,
            retail_url=pydantic.AnyUrl("https://jerryshardware.com/product/3690"),
            retailer_name="Jerry's Hardware",
        ),
    ]
    assert gpu_listing_data_no_retail_url == [
        GpuListingData(
            gpu_name="MSI Radeon RX 6700 XT",
            gpu_price=68000,
            retail_url=pydantic.AnyUrl("https://jerryshardware.com/product/3690"),
            retailer_name="Jerry's Hardware",
        ),
        GpuListingData(
            gpu_name="Zotac Geforce RTX 4060",
            gpu_price=48000,
            retail_url=pydantic.AnyUrl("https://powerpc.com/product/3301"),
            retailer_name="Jerry's Hardware",
        ),
    ]


def test_wrong_tag_name_elem_does_not_exist_error(
    no_missing_in_card: list[Tag],
):
    gpu_list_attrs_test = GpuListingAttrs(
        gpu_name_css_sel="li.gpu-name",
        gpu_price_css_sel="li.gpu-pricing",
        retail_url_css_sel="li.product-url > a",
        retailer_name="Jerry's Hardware",
    )
    with pytest.raises(ElementDoesNotExistError):
        gpu_list_attrs_test.get_gpu_listing_data(no_missing_in_card)


def test_multiple_gpu_attrs_missing(
    missing_multipe_in_card: list[Tag],
):
    gpu_list_attrs_test = GpuListingAttrs(
        gpu_name_css_sel="li.gpu-name",
        gpu_price_css_sel="li.gpu-price",
        retail_url_css_sel="li.product-url > a",
        retailer_name="Jerry's Hardware",
    )
    gpu_listing_data_multi_missing = gpu_list_attrs_test.get_gpu_listing_data(
        missing_multipe_in_card
    )
    assert gpu_listing_data_multi_missing == [
        GpuListingData(
            gpu_name="Zotac Geforce RTX 4060",
            gpu_price=48000,
            retail_url=pydantic.AnyUrl("https://powerpc.com/product/3301"),
            retailer_name="Jerry's Hardware",
        ),
    ]


def test_get_price_int_regex():
    assert get_price_int_regex("28,000") == "28000"
    assert get_price_int_regex("69000") == "69000"
    assert get_price_int_regex("BDT. 50000") == "50000"
    assert get_price_int_regex("BDT100,000") == "100000"


# TODO: need to add a test where all the texts are complete
