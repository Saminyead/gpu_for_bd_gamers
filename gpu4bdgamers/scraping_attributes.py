import dataclasses

import requests
from bs4 import BeautifulSoup

from typing import Literal, Callable

class NextPageUrlTagStrCssSelError(Exception):
    def __init__(self) -> None:
        super().__init__(
            """You have either specified both next_page_url_tag_str and 
            next_page_url_css_sel or both are None. Please specify a value
            for one and only one of the fields."""
        )

@dataclasses.dataclass
class ScrapingAttributes:
    first_page_url: str
    card_css_sel: str
    gpu_name_css_sel: str
    gpu_price_css_sel: str
    retailer_name: str
    next_page_url_tag_str: str|None = None
    next_page_url_css_sel: str|None = None

    @staticmethod
    def _get_page_soup(url:str) -> BeautifulSoup:
        """Get the contents of a page and return a BeautifulSoup object"""
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content,features='html.parser')
        return soup
    
    def _scrape_pages(
        self,
        search_strategy:Literal['find_all','select'],
        **kwargs
    ) -> list[BeautifulSoup]:
        """Use the find_all() BeautifulSoup method to get a list of soup
        objects from the first page url"""
        next_page_url = self.first_page_url
        soup_list: list[BeautifulSoup] = []
        while True:
            current_page_soup = self._get_page_soup(next_page_url)
            soup_list.append(current_page_soup)
            # best way to inject find_all/select method
            search_method = getattr(current_page_soup,search_strategy)
            next_page_url_result_set = search_method(**kwargs)
            if not next_page_url_result_set:
                break
            next_page_url = next_page_url_result_set[0]['href']
        return soup_list
    
    def get_pages(self) -> list[BeautifulSoup]:
        """Starts with the first page url, and then scrapes all pages until it
        no longer finds a next page. Returns a list of pages as a list of 
        BeautifulSoup objects"""
        if ((
            not self.next_page_url_tag_str and not self.next_page_url_css_sel
        ) or (self.next_page_url_tag_str and self.next_page_url_css_sel)):
            raise NextPageUrlTagStrCssSelError