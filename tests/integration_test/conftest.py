import pandas as pd
import requests

import toml
from gpu4bdgamers.data_coll_script import get_master_df, data_collection_to_df

import pytest

import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
with open(CURRENT_DIR/'scraping_config.toml','r') as f:
    scraping_config_contents = toml.load(f)

FIRST_PAGE_URLS = scraping_config_contents['first_page_urls']
CARD_CSS_SELECTORS = scraping_config_contents['card_css_selectors']

RADEON_GPU_LIST_FILE_TEST = CURRENT_DIR/'gpu_units_of_interest'/'geforce_gpu_units.txt'
GEFORCE_GPU_LIST_FILE_TEST = CURRENT_DIR/'gpu_units_of_interest'/'radeon_gpu_units.txt'
INTEL_GPU_LIST_FILE_TEST = CURRENT_DIR/'gpu_units_of_interest'/'intel_gpu_units.txt'

master_df:pd.DataFrame = get_master_df(FIRST_PAGE_URLS,CARD_CSS_SELECTORS)
DF_DICT_TEST = data_collection_to_df(
    master_df, 
    RADEON_GPU_LIST_FILE_TEST, 
    GEFORCE_GPU_LIST_FILE_TEST, 
    INTEL_GPU_LIST_FILE_TEST
)

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