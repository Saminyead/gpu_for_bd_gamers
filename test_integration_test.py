import pytest

from data_coll_script import data_collection_to_df, data_collection_to_db

import os
import dotenv

import pandas as pd
import datetime
import sqlalchemy


dotenv.load_dotenv("test.env")
test_db_url = os.getenv("test_db_url")



def df_dict_test(
) -> dict[str,pd.DataFrame]:
    """Fixture for getting the dictionary of dataframes to
    either push to database, or append them"""
    # the data_collection_to_db needs to be tested in the future
    # fixture will need to change then
    return data_collection_to_df()


TEST_DF_DICT = df_dict_test()
TEST_DF_DICT_TO_APPEND = {
    "gpu_of_interest": TEST_DF_DICT['gpu_of_interest'],
    "lowest_prices" : TEST_DF_DICT['lowest_prices'],
}
TEST_DF_DICT_TO_REPLACE = {
    "lowest_prices_tiered": TEST_DF_DICT['lowest_prices_tiered']
}


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
    metadata = sqlalchemy.MetaData()
    
    db_table_list = [
        sqlalchemy.Table(
            table_name,
            metadata,
            sqlalchemy.Column('retail_url',sqlalchemy.String,primary_key=True),
            sqlalchemy.Column('data_collection_date',sqlalchemy.String),
        ) 
        for table_name in list_of_table_names
    ]
    
    for table in db_table_list:
        delete_rows = table.delete().where(table.c.data_collection_date == today)
        conn.execute(delete_rows)



def test_push_to_db_no_today_data_tables(
        test_df_dict_to_append:dict[str,pd.DataFrame]=TEST_DF_DICT_TO_APPEND,
        test_df_dict_to_replace:dict[str,pd.DataFrame]=TEST_DF_DICT_TO_REPLACE,
        test_db_url:str = test_db_url,
    ):
    """Tests that pushing to database works when there is no data for
    'today' in the database table"""

    #    - one for no pre-existing data
    #       - test push_to_db, and clear dataframe after the test
    #       - perhaps the existing ones can be cleared for this

    db_conn = sqlalchemy.create_engine(test_db_url).connect()
    list_table_names = test_df_dict_to_append.keys() + \
        test_df_dict_to_replace.keys()
    
    delete_db_today_rows(db_conn,list_table_names)

    data_collection_to_db(
        test_db_url,
        test_df_dict_to_append,
        test_df_dict_to_replace
    )



    gpu_of_interest_df = pd.read_sql(
        sql=sql_query_format("gpu_of_interest"),
        con=db_conn
    )

    lowest_prices_df = pd.read_sql(
        sql=sql_query_format("lowest_prices"),
        con=db_conn
    )

    lowest_prices_tiered = pd.read_sql(
        sql=sql_query_format("lowest_prices_tiered"),
        con=db_conn
    )

    assert len(gpu_of_interest_df) != 0
    assert len(lowest_prices_df) != 0
    assert len(lowest_prices_tiered) != 0


# TODO:
#    - create two database sets of tables for each of the dataframes
#    - one for pre-existing data
#       - should raise error when trying to push