import pytest
from gpu4bdgamers.scraping import (
    get_page_soup_list,
    get_card_list,
    ElementDoesNotExistError,
)

from bs4 import BeautifulSoup


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
