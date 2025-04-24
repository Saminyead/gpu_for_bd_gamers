import dataclasses

import requests

from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from typing import Literal

class NextPageUrlTagStrCssSelError(Exception):
    def __init__(self) -> None:
        super().__init__(
            """You have either specified both next_page_url_tag_str and 
            next_page_url_css_sel or both are None. Please specify a value
            for one and only one of the fields."""
        )

@dataclasses.dataclass(slots = True)
class ScrapingAttributes:
    first_page_url: str
    next_pg_sel: str
    card_css_sel: str
    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retailer_name: str

    def get_page_soup(self:'ScrapingAttributes') -> list[BeautifulSoup]:
        """Get the contents of a page and return a BeautifulSoup object"""
        soup_list = []
        next_page_url = self.first_page_url
        while next_page_url:
            page_content = requests.get(next_page_url).content
            soup = BeautifulSoup(page_content, features = 'html.parser')
            soup_list.append(soup)
            next_page_url = soup.select(self.next_pg_sel)[0]['href']
        return soup_list 
    
    def get_cards(self,soup_list:list[BeautifulSoup]) -> list[Tag]:
        """Get a list of cards from a list of beautiful soup objects(pages)"""
        card_list = []
        for page in soup_list:
            cards  = page.select(self.card_css_sel)
            card_list.extend(cards)
        return card_list
    
    # TODO: method for getting name and price
