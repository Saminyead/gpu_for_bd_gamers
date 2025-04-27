import dataclasses

import requests

from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from typing import Literal


@dataclasses.dataclass(slots=True)
class ScrapingAttributes:
    first_page_url: str
    next_page_css_sel: str
    card_css_sel: str
    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retailer_name: str

    def get_page_soup(self: "ScrapingAttributes") -> list[BeautifulSoup]:
        """Get the contents of a page and return a BeautifulSoup object"""
        soup_list = []
        next_page_url = self.first_page_url
        while next_page_url:
            page_content = requests.get(next_page_url).content
            soup = BeautifulSoup(page_content, features="html.parser")
            soup_list.append(soup)
            next_page_url = soup.select(self.next_page_css_sel)[0]["href"]
        return soup_list

    def get_cards(self, soup_list: list[BeautifulSoup]) -> list[Tag]:
        """Get a list of cards from a list of beautiful soup objects(pages)"""
        card_list = []
        for page in soup_list:
            cards = page.select(self.card_css_sel)
            card_list.extend(cards)
        return card_list


def get_page_soup_list(
    first_page_url: str, next_page_url_sel: str
) -> list[BeautifulSoup]:
    """Starting from the first page, this function will navigate through
    all the GPU listing pages of a retailer website by finding the next
    page URL (through the next_page_url_sel selector) and return a list of
    BeautifulSoup objects of the contents of the pages."""
    # soup_list = []
    # next_page_url = first_page_url
    # while next_page_url:
    #     page_content = requests.get(next_page_url).content
    #     soup = BeautifulSoup(page_content, features="html.parser")
    #     soup_list.append(soup)
    #     next_page_url_elem = soup.select_one(next_page_url_sel)
    #     if not next_page_url_elem:
    #         raise ElementDoesNotExistError(f"Unable to find next page element with selector {next_page_url_sel}")
    #     next_page_url = next_page_url_elem['href']
    # return soup_list
    requests.get(first_page_url)

class ElementDoesNotExistError(Exception):
    pass
