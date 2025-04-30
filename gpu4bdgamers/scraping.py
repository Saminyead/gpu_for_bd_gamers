import dataclasses
import pydantic

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
) -> list[Tag]:
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


@dataclasses.dataclass
class GpuListingAttrs:
    """CSS selectors of the GPU name, price, and retail url."""

    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retail_url_css_sel: str

    def get_gpu_listing_data(self, card_list: list[Tag]):
        gpu_listing_list = []
        for card in card_list:
            gpu_name_tag = card.select_one(self.gpu_name_css_sel)
            gpu_price_tag = card.select_one(self.gpu_name_css_sel)
            retail_url_tag = card.select_one(self.retail_url_css_sel)
            if not gpu_name_tag or not gpu_price_tag or not retail_url_tag:
                raise ElementDoesNotExistError(
                    "Either gpu name, price or retail url does not exist."
                )
            gpu_name = gpu_name_tag.text
            gpu_price = gpu_price_tag.text
            retail_url = retail_url_tag["href"]
            # gpu_listing = GpuListingData(
            #     gpu_name=gpu_name, gpu_price=gpu_price, retail_url=retail_url
            # )
            # gpu_listing_list.append(gpu_listing)
        # return gpu_listing_list


class GpuListingData(pydantic.BaseModel):
    gpu_name: str
    gpu_price: int
    retail_url: pydantic.AnyUrl


class ElementDoesNotExistError(Exception):
    pass
