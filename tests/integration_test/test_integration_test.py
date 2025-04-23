from logging import RootLogger
import pathlib
import pytest

# TODO: we will add a different test for data_collection_to_df
from gpu4bdgamers.data_coll_script import (
    data_collection_to_df, data_collection_to_db
)
from gpu4bdgamers.database import push_to_db, TodayDataAlreadyExistsError

import pandas as pd
import pandas.testing as pdt
import datetime
import sqlalchemy


def sql_query_format(table_name:str):
    """formats the sql query so we can just plug in table_name 
    in test_main"""
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    return f"SELECT * FROM {table_name} WHERE data_collection_date = '{today}'"


def delete_db_today_rows(
        conn:sqlalchemy.engine.base.Connection,
        list_of_table_names:list[str],
) -> None:
    """deletes all rows with today's date in a database table"""
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    metadata = sqlalchemy.MetaData(bind = conn)

    metadata.reflect(bind = conn)

    
    db_table_list = list(metadata.tables.keys())    
    if not db_table_list:
        return
    for table in db_table_list:
        delete_rows = table.delete().where(table.c.data_collection_date == today)
        conn.execute(delete_rows)



def test_push_to_db_no_today_data_tables(
        mock_master_df: pd.DataFrame,
        geforce_units_of_interest_file_path:pathlib.Path,
        radeon_units_of_interest_file_path:pathlib.Path,
        intel_units_of_interest_file_path:pathlib.Path,
        test_logger:RootLogger,
        test_tier_score_excel_file_path:pathlib.Path,
        expected_gpu_of_interest_df:pd.DataFrame,
        expected_lowest_prices_df:pd.DataFrame,
        expected_lowest_prices_tiered_df:pd.DataFrame,
        test_db_url:str,
        test_db_conn:sqlalchemy.engine.Connection,
        tables_to_create:None
    ):
    """Tests that pushing to database works when there is no data for
    'today' in the database table. Also tests if GPU units are properly prefixed
    e.g. Geforce are not prefixed by RX etc."""
    df_dict_to_push = data_collection_to_df(
        master_df = mock_master_df,
        geforce_gpu_units_filepath = geforce_units_of_interest_file_path,
        radeon_gpu_units_filepath = radeon_units_of_interest_file_path,
        intel_gpu_units_filepath = intel_units_of_interest_file_path,
        logger = test_logger,
        tier_score_excel_file = test_tier_score_excel_file_path
    )
    df_to_append_dict = {
        "gpu_of_interest": df_dict_to_push['gpu_of_interest'],
        "lowest_prices" : df_dict_to_push['lowest_prices'],
    }
    df_to_replace_dict = { "lowest_prices_tiered" : df_dict_to_push['lowest_prices_tiered']}
    data_collection_to_db(
        db_url = test_db_url,
        df_table_to_append_dict = df_to_append_dict,
        df_table_to_replace_dict = df_to_replace_dict,
        logger = test_logger
    )

    obtained_gpu_of_interest_df = df_dict_to_push['gpu_of_interest'].\
        sort_values(by="gpu_price",ignore_index=True)
    obtained_lowest_prices_df = df_dict_to_push['lowest_prices'].\
        sort_values(by="gpu_price",ignore_index=True)
    obtained_lowest_prices_tiered_df = df_dict_to_push['lowest_prices_tiered'].\
        sort_values(by="gpu_price",ignore_index=True)

    assert obtained_gpu_of_interest_df.equals(expected_gpu_of_interest_df)
    assert obtained_lowest_prices_df.equals(expected_lowest_prices_df)
    # best way to compare dataframes with floating point values
    pdt.assert_frame_equal(
        obtained_lowest_prices_tiered_df, expected_lowest_prices_tiered_df,
        rtol = 0.001, atol = 0.001  # for us, max tolerance could be 0.01
    )

    pdt.assert_frame_equal(
        left = pd.read_sql(
            sql = "SELECT * FROM gpu_of_interest",
            con = test_db_conn
        ).sort_values(by="gpu_price",ignore_index=True),
        right = expected_gpu_of_interest_df
    )
    pdt.assert_frame_equal(
        left = pd.read_sql(
            sql = "SELECT * FROM lowest_prices",
            con = test_db_conn
        ).sort_values(by="gpu_price",ignore_index=True),
        right = expected_lowest_prices_df
    )
    pdt.assert_frame_equal(
        left = pd.read_sql(
            sql = "SELECT * FROM lowest_prices_tiered",
            con = test_db_conn
        ).sort_values(by="gpu_price",ignore_index=True),
        right = expected_lowest_prices_tiered_df
    )

@pytest.mark.skip
def test_push_to_db_fail_today_exists(
    expected_gpu_of_interest_df:pd.DataFrame,
    expected_lowest_prices_df:pd.DataFrame,
    expected_lowest_prices_tiered_df:pd.DataFrame,
    gpu_data_coll_test_logger: RootLogger,
    test_db_url:str,
    test_db_conn:sqlalchemy.engine.mock.MockConnection,
) -> None:
    """Test for pushing to database table where 'today' data already exists"""
    

    with pytest.raises(TodayDataAlreadyExistsError):
        push_to_db(db_conn,gpu_data_coll_test_logger,**df_dict_test)
