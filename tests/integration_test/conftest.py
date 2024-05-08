import pandas as pd
import requests

import toml
from gpu4bdgamers.data_coll_script import get_master_df, data_collection_to_df

import pytest

with open('scraping_config.toml','r') as f:
    scraping_config_contents = toml.load(f)

FIRST_PAGE_URLS = scraping_config_contents['first_page_urls']
CARD_CSS_SELECTORS = scraping_config_contents['card_css_selectors']

master_df:pd.DataFrame = get_master_df(FIRST_PAGE_URLS,CARD_CSS_SELECTORS)
DF_DICT_TEST = data_collection_to_df(master_df)

@pytest.fixture
def df_dict_test(df_dict:dict=DF_DICT_TEST):
    return df_dict

@pytest.fixture
def df_dict_to_append_test(test_df_dict:dict=DF_DICT_TEST):
    return {
        "gpu_of_interest": test_df_dict['gpu_of_interest'],
        "lowest_prices": test_df_dict['lowest_prices']
    }

@pytest.fixture
def df_dict_to_replace_test(test_df_dict:dict=DF_DICT_TEST):
    return {
        "lowest_prices_tiered": test_df_dict['lowest_prices_tiered']
    }