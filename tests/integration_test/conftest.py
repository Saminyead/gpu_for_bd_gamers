import pandas as pd

import pytest

import pandas as pd

import pathlib
from logging import RootLogger
from datetime import datetime

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
GPU_OF_INTEREST_FILES_DIR = CURRENT_DIR / 'gpu_units_of_interest'
DATA_DIR = CURRENT_DIR / 'data'
EXPECTED_DATA_DIR = DATA_DIR / 'expected'

def add_data_collection_row(filepath:pathlib.Path, position:int = 3):
    df = pd.read_csv(filepath)
    date_col = [datetime.today().strftime("%Y-%m-%d")] * len(df)
    df.insert(loc = position, column = "data_collection_date", value = date_col)
    return df

@pytest.fixture
def geforce_units_of_interest_file_path(
    filepath: pathlib.Path = GPU_OF_INTEREST_FILES_DIR / 'geforce_gpu_units.txt'
):
    return filepath

@pytest.fixture
def radeon_units_of_interest_file_path(
    filepath: pathlib.Path = GPU_OF_INTEREST_FILES_DIR / 'radeon_gpu_units.txt'
):
    return filepath

@pytest.fixture
def intel_units_of_interest_file_path(
    filepath: pathlib.Path = GPU_OF_INTEREST_FILES_DIR / 'intel_gpu_units.txt'
):
    return filepath

@pytest.fixture
def test_tier_score_excel_file_path(
    filepath: pathlib.Path = DATA_DIR / 'tier_score.xlsx'
):
    return filepath

@pytest.fixture
def test_db_url(curr_dir:pathlib.Path = CURRENT_DIR):
    return f"sqlite:///{curr_dir}/test_db.db"

@pytest.fixture
def mock_master_df(filepath:pathlib.Path = DATA_DIR / 'gpu_prices.csv'):
    return add_data_collection_row(filepath)

@pytest.fixture
def expected_gpu_of_interest_df(
    filepath:pathlib.Path = EXPECTED_DATA_DIR / 'gpu_units_of_interest.csv'
):
    return add_data_collection_row(filepath)

@pytest.fixture
def expected_lowest_prices_df(
    filepath:pathlib.Path = EXPECTED_DATA_DIR / 'lowest_prices.csv'
):
    return add_data_collection_row(filepath)


@pytest.fixture
def expected_lowest_prices_tiered_df(
    filepath:pathlib.Path = EXPECTED_DATA_DIR / 'lowest_prices_tiered.csv'
):
    return add_data_collection_row(filepath)

@pytest.fixture
def test_logger():
    return RootLogger(0)
