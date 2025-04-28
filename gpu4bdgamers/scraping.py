import dataclasses

import requests

from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from typing import Literal


def get_page_soup_list(
    first_page_url: str, next_page_url_sel: str
) -> list[BeautifulSoup]:
    """Starting from the first page, this function will navigate through
    all the GPU listing pages of a retailer website by finding the next
    page URL (through the next_page_url_sel selector) and return a list of
    BeautifulSoup objects of the contents of the pages."""
    soup_list = []
    next_page_url = first_page_url
    while next_page_url:
        page_content = requests.get(next_page_url).content
        soup = BeautifulSoup(page_content, features="html.parser")
        soup_list.append(soup)
        next_page_url_elem = soup.select_one(next_page_url_sel)
        if not next_page_url_elem:
            raise ElementDoesNotExistError(
                f"Unable to find next page element with selector {next_page_url_sel}"
            )
        next_page_url = next_page_url_elem["href"]
    return soup_list


def get_card_list(
    soup_list: list[BeautifulSoup],
    card_css_sel: str,
):
    """A card is a section of the page that contains all the information
    regarding a listed GPU."""
    card_list = []
    for soup in soup_list:
        card_list_in_soup = soup.select(card_css_sel)
        if not card_list_in_soup:
            raise ElementDoesNotExistError(
                f"""Unable to find any card with selector {card_css_sel} in one
                of the pages."""
            )
        card_list.extend(card_list_in_soup)
    return card_list


class ElementDoesNotExistError(Exception):
    pass
