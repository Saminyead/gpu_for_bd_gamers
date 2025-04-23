import pandas as pd

import pytest

import pandas as pd

import pathlib
from logging import RootLogger
from datetime import datetime

import sqlalchemy

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
    df = add_data_collection_row(filepath)
    df = df.sort_values(by = "gpu_price", ignore_index = True)
    return df

@pytest.fixture
def expected_lowest_prices_df(
    filepath:pathlib.Path = EXPECTED_DATA_DIR / 'lowest_prices.csv'
):
    df = add_data_collection_row(filepath)
    df = df.sort_values(by = "gpu_price", ignore_index = True)
    return df

@pytest.fixture
def expected_lowest_prices_tiered_df(
    filepath:pathlib.Path = EXPECTED_DATA_DIR / 'lowest_prices_tiered.csv'
):
    df = add_data_collection_row(filepath)
    df = df.sort_values(by = "gpu_price", ignore_index = True)
    return df

@pytest.fixture
def test_db_conn(test_db_url:pathlib.Path) -> sqlalchemy.engine.mock.MockConnection:
    engine = sqlalchemy.create_engine(url = test_db_url)
    return engine.connect()

@pytest.fixture()
def test_db_metadata(
    test_db_conn:sqlalchemy.engine.mock.MockConnection
) -> sqlalchemy.MetaData:
    return sqlalchemy.MetaData(bind = test_db_conn)

@pytest.fixture()
def gpu_of_interest_table(test_db_metadata:sqlalchemy.MetaData):
    table = sqlalchemy.Table(
        "gpu_of_interest", test_db_metadata,
        sqlalchemy.Column("gpu_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_price", sqlalchemy.Integer),
        sqlalchemy.Column("retail_url", sqlalchemy.String, primary_key = True),
        sqlalchemy.Column("data_collection_date", sqlalchemy.String),
        sqlalchemy.Column("retailer_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_unit_name", sqlalchemy.String),
    )
    return table

@pytest.fixture()
def lowest_prices_table(test_db_metadata:sqlalchemy.MetaData):
    table = sqlalchemy.Table(
        "lowest_prices", test_db_metadata,
        sqlalchemy.Column("gpu_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_price", sqlalchemy.Integer),
        sqlalchemy.Column("retail_url", sqlalchemy.String, primary_key = True),
        sqlalchemy.Column("data_collection_date", sqlalchemy.String),
        sqlalchemy.Column("retailer_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_unit_name", sqlalchemy.String),
    )
    return table

@pytest.fixture()
def lowest_prices_tiered_table(test_db_metadata:sqlalchemy.MetaData):
    table = sqlalchemy.Table(
        "lowest_prices_tiered", test_db_metadata,
        sqlalchemy.Column("gpu_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_price", sqlalchemy.Integer),
        sqlalchemy.Column("retail_url", sqlalchemy.String, primary_key = True),
        sqlalchemy.Column("data_collection_date", sqlalchemy.String),
        sqlalchemy.Column("retailer_name", sqlalchemy.String),
        sqlalchemy.Column("gpu_unit_name", sqlalchemy.String),
        sqlalchemy.Column("base_tier_score", sqlalchemy.Float),
        sqlalchemy.Column("net_tier_score", sqlalchemy.Float),
        sqlalchemy.Column("non_rt_net_score", sqlalchemy.Float),
        sqlalchemy.Column("price_per_base_tier", sqlalchemy.Float),
        sqlalchemy.Column("price_per_net_tier", sqlalchemy.Float),
        sqlalchemy.Column("price_per_non_rt_tier", sqlalchemy.Float),
    )
    return table

@pytest.fixture(scope = 'function')
def tables_to_create(
    test_db_metadata:sqlalchemy.MetaData,
    gpu_of_interest_table:sqlalchemy.Table,
    lowest_prices_table:sqlalchemy.Table,
    lowest_prices_tiered_table:sqlalchemy.Table
):
    test_db_metadata.create_all()
    yield
    test_db_metadata.drop_all()

@pytest.fixture(scope = 'function')
def insert_today_data_stmts(
        test_db_conn:sqlalchemy.engine.mock.MockConnection,
        test_db_metadata: sqlalchemy.MetaData,
        gpu_of_interest_table:sqlalchemy.Table,
        lowest_prices_table:sqlalchemy.Table,
        lowest_prices_tiered_table:sqlalchemy.Table
):
    test_db_metadata.create_all()
    gpu_of_interest_insert = sqlalchemy.insert(gpu_of_interest_table).values(
        gpu_name = "ASUS ROG Geforce RTX 3090 Ti",
        gpu_price = 200000,
        retail_url = "https://startechbangladesh.com/product/5870",
        data_collection_date = datetime.today().strftime("%Y-%m-%d"),
        retailer_name = "Startech Bangladesh",
        gpu_unit_name = "Geforce RTX 3090 Ti"
    )
    lowest_prices_insert = sqlalchemy.insert(lowest_prices_table).values(
        gpu_name = "ASUS ROG Geforce RTX 3090 Ti",
        gpu_price = 200000,
        retail_url = "https://startechbangladesh.com/product/5870",
        data_collection_date = datetime.today().strftime("%Y-%m-%d"),
        retailer_name = "Startech Bangladesh",
        gpu_unit_name = "Geforce RTX 3090 Ti"
    )
    lowest_prices_tiered_insert = sqlalchemy.insert(lowest_prices_tiered_table).values(
        gpu_name = "ASUS ROG Geforce RTX 3090 Ti",
        gpu_price = 200000,
        retail_url = "https://startechbangladesh.com/product/5870",
        data_collection_date = datetime.today().strftime("%Y-%m-%d"),
        retailer_name = "Startech Bangladesh",
        gpu_unit_name = "Geforce RTX 3090 Ti",
        base_tier_score = 10,
        net_tier_score = 15,
        non_rt_net_score = 12.5,
        price_per_base_tier = 20000,
        price_per_net_tier = 13333.3333,
        price_per_non_rt_tier = 16000
    )
    yield [gpu_of_interest_insert, lowest_prices_insert, lowest_prices_tiered_insert]
    test_db_metadata.drop_all()

@pytest.fixture
def test_logger():
    return RootLogger(0)
