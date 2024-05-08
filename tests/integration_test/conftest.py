import pandas as pd
import requests

import toml
from gpu4bdgamers.data_coll_script import get_master_df

import pytest

with open('scraping_config.toml','r') as f:
    scraping_config_contents = toml.load(f)

FIRST_PAGE_URLS = scraping_config_contents['first_page_urls']
CARD_CSS_SELECTORS = scraping_config_contents['card_css_selectors']

@pytest.fixture
def master_df(
        first_page_urls:dict[str,str] = FIRST_PAGE_URLS,
        card_css_selectors:dict[str,str] = CARD_CSS_SELECTORS
) -> pd.DataFrame:
    
    return get_master_df(first_page_urls,card_css_selectors)