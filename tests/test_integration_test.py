import pytest

from data_coll_script import data_collection_to_df, data_collection_to_db
from database import push_to_db, TodayDataAlreadyExistsError

import os
import dotenv

import pandas as pd
import datetime
import sqlalchemy


dotenv.load_dotenv("test.env")
test_db_url = os.getenv("test_db_url")


TEST_DF_DICT = data_collection_to_df()
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

    
    with sqlalchemy.create_engine(test_db_url).connect() as db_conn:
        list_table_names = list(test_df_dict_to_append.keys()) +\
            list(test_df_dict_to_replace.keys())
        
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

    

def test_push_to_db_fail_today_exists(
    test_db_url:str = test_db_url,
    test_df_dict:dict[str,pd.DataFrame] = TEST_DF_DICT
) -> None:
    """Test for pushing to database table where 'today' data already exists"""
    list_df_name_today_exists = [
        f"{df_name}_today_exists" for df_name in test_df_dict.keys()
    ]

    with sqlalchemy.create_engine(test_db_url).connect() as db_conn:
        for df_name_today,df_name_og in \
            zip(list_df_name_today_exists, test_df_dict.keys()):

            test_df_dict[df_name_og].to_sql(
                name=df_name_today,
                con=db_conn,
                if_exists='append',
                index=False
            )

        with pytest.raises(TodayDataAlreadyExistsError):
            push_to_db(db_conn,**test_df_dict)