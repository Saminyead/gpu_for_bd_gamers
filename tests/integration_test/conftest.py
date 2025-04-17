import pandas as pd

import pytest

import pathlib
from logging import RootLogger
from datetime import datetime

import sqlalchemy

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

@pytest.fixture
def test_db_url(curr_dir:pathlib.Path = CURRENT_DIR):
    return f"sqlite:///{curr_dir}/test_db.db"

@pytest.fixture
def gpu_of_interest_df() -> pd.DataFrame:
    return pd.DataFrame(data = {
        "gpu_unit_name": [
            "XFX Radeon RX 570", "MSI Radeon RX 6700 XT", "Zotac GeForce RTX 4070", 
            "Bionic GeForce RTX 3060", "Intel Arc A770", "Froststar Intel Arc A750", 
            "Asus ROG Radeon RX 6800", "Asus ROG GeForce RTX 4070"
        ],
        "data_collection_date": [datetime.today().strftime("%Y-%m-%d")] * 8
    })

@pytest.fixture
def lowest_prices_df() -> pd.DataFrame:
    return pd.DataFrame(data = {
        "gpu_unit_name": [
            "XFX Radeon RX 570", "MSI Radeon RX 6700 XT", "Zotac GeForce RTX 4070", 
            "Bionic GeForce RTX 3060", "Intel Arc A770", "Froststar Intel Arc A750", 
            "Asus ROG Radeon RX 6800", "Asus ROG GeForce RTX 4070"
        ],
        "data_collection_date": [datetime.today().strftime("%Y-%m-%d")] * 8
    })

@pytest.fixture
def lowest_prices_tiered_df() -> pd.DataFrame:
    return pd.DataFrame(data = {
        "gpu_unit_name": [
            "XFX Radeon RX 570", "MSI Radeon RX 6700 XT", "Zotac GeForce RTX 4070", 
            "Bionic GeForce RTX 3060", "Intel Arc A770", "Froststar Intel Arc A750", 
            "Asus ROG Radeon RX 6800", "Asus ROG GeForce RTX 4070"
        ],
        "data_collection_date": [datetime.today().strftime("%Y-%m-%d")] * 8
    })


@pytest.fixture
def df_dict_to_append_test(
    gpu_of_interest_df:pd.DataFrame, lowest_prices_df:pd.DataFrame
):
    return {
        "gpu_of_interest": gpu_of_interest_df,
        "lowest_prices": lowest_prices_df
    }

@pytest.fixture
def df_dict_to_replace_test(lowest_prices_tiered_df:pd.DataFrame):
    return {
        "lowest_prices_tiered": lowest_prices_tiered_df
    }

@pytest.fixture
def gpu_data_coll_test_logger():
    return RootLogger(0)

@pytest.fixture(scope = "function")
def db_conn(test_db_url:str):
    return sqlalchemy.create_engine(test_db_url).connect()

@pytest.fixture(scope = "function")
def db_metadata():
    return sqlalchemy.MetaData()

@pytest.fixture
def gpu_unit_name_col():
    return sqlalchemy.Column("gpu_unit_name", sqlalchemy.String(1000))

@pytest.fixture
def data_collection_date_col():
    return sqlalchemy.Column("data_collection_date", sqlalchemy.String(200))

@pytest.fixture(scope = "function")
def gpu_of_interest_table(
    db_metadata : sqlalchemy.MetaData,
    gpu_unit_name_col : sqlalchemy.Column,
    data_collection_date_col : sqlalchemy.Column
):
    return sqlalchemy.Table(
        "gpu_of_interest", db_metadata, gpu_unit_name_col, 
        data_collection_date_col
    )

@pytest.fixture(scope = "function")
def lowest_prices_table(
    db_metadata : sqlalchemy.MetaData,
    gpu_unit_name_col : sqlalchemy.Column,
    data_collection_date_col : sqlalchemy.Column
):
    return sqlalchemy.Table(
        "lowest_prices", db_metadata, gpu_unit_name_col.copy(), 
        data_collection_date_col.copy()
    )

@pytest.fixture(scope = "function")
def lowest_prices_tiered_table(
    db_metadata : sqlalchemy.MetaData,
    gpu_unit_name_col : sqlalchemy.Column,
    data_collection_date_col : sqlalchemy.Column
):
    return sqlalchemy.Table(
        "lowest_prices_tiered", db_metadata, gpu_unit_name_col.copy(),
        data_collection_date_col.copy()
    )

@pytest.fixture(scope = "function")
def no_today_tables_conn(
    db_conn,
    db_metadata,
    gpu_of_interest_table,
    lowest_prices_table,
    lowest_prices_tiered_table
):
    db_metadata.create_all(db_conn)
    yield db_conn
    db_metadata.drop_all(db_conn)
    db_conn.close()

