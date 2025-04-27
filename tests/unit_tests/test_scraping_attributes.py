import pytest
from gpu4bdgamers.scraping import (
    get_page_soup_list, ElementDoesNotExistError
)


def test_element_does_not_exist_error_is_raised(mock_server, no_next_page_url:str):
    with pytest.raises(ElementDoesNotExistError):
        get_page_soup_list(no_next_page_url, "div")
