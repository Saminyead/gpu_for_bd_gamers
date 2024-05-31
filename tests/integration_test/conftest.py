import pandas as pd
import requests

import toml
from gpu4bdgamers.data_coll_script import get_master_df, data_collection_to_df

from logging import RootLogger
from gpu4bdgamers.logger import setup_logging

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

TEST_LOGS_DIR = pathlib.Path(__file__).parent/'logs'

@pytest.fixture
def gpu_data_coll_test_logger(
    log_dir=TEST_LOGS_DIR,
    log_filename="gpu_data_coll_script.log"
) -> RootLogger:
    return setup_logging(log_filename, log_dir)

@pytest.fixture
def test_master_df(
    gpu_data_coll_test_logger:RootLogger,
    first_pg_urls:dict=FIRST_PAGE_URLS,
    card_css_sels:dict=CARD_CSS_SELECTORS,
) -> pd.DataFrame:
    return get_master_df(
        first_pg_urls, card_css_sels, gpu_data_coll_test_logger
    )



@pytest.fixture
def df_dict_test(
    test_master_df:pd.DataFrame,
    gpu_data_coll_test_logger:RootLogger,
    geforce_gpu_list_file:pathlib.Path = GEFORCE_GPU_LIST_FILE_TEST,
    radeon_gpu_list_file:pathlib.Path = RADEON_GPU_LIST_FILE_TEST,
    intel_gpu_list_file:pathlib.Path = INTEL_GPU_LIST_FILE_TEST,
) -> dict[str, pd.DataFrame]:
    return data_collection_to_df(
        test_master_df,
        geforce_gpu_list_file,
        radeon_gpu_list_file,
        intel_gpu_list_file,
        gpu_data_coll_test_logger
    )

@pytest.fixture
def df_dict_to_append_test(df_dict_test:dict):
    return {
        "gpu_of_interest": df_dict_test['gpu_of_interest'],
        "lowest_prices": df_dict_test['lowest_prices']
    }

@pytest.fixture
def df_dict_to_replace_test(df_dict_test:dict):
    return {
        "lowest_prices_tiered": df_dict_test['lowest_prices_tiered']
    }