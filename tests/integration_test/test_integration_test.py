from logging import RootLogger
import pytest

# TODO: we will add a different test for data_collection_to_df
from gpu4bdgamers.data_coll_script import (
    data_collection_to_df, data_collection_to_db
)
from gpu4bdgamers.database import push_to_db, TodayDataAlreadyExistsError

import pandas as pd
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
        df_dict_to_append_test:dict[str,pd.DataFrame],
        df_dict_to_replace_test:dict[str,pd.DataFrame],
        gpu_data_coll_test_logger:RootLogger,
        test_db_url:str,
        no_today_tables_conn: sqlalchemy.engine.Connection
    ):
    """Tests that pushing to database works when there is no data for
    'today' in the database table. Also tests if GPU units are properly prefixed
    e.g. Geforce are not prefixed by RX etc."""
    data_collection_to_db(
        test_db_url,
        df_dict_to_append_test,
        df_dict_to_replace_test,
        gpu_data_coll_test_logger
    )

    gpu_of_interest_df = pd.read_sql(
        sql=sql_query_format("gpu_of_interest"),
        con=no_today_tables_conn
    )
    lowest_prices_df = pd.read_sql(
        sql=sql_query_format("lowest_prices"),
        con=no_today_tables_conn
    )
    lowest_prices_tiered = pd.read_sql(
        sql=sql_query_format("lowest_prices_tiered"),
        con=no_today_tables_conn
    )

    assert len(gpu_of_interest_df) != 0
    assert len(lowest_prices_df) != 0
    assert len(lowest_prices_tiered) != 0

def test_push_to_db_fail_today_exists(
    df_dict_test:dict[str,pd.DataFrame],
    gpu_data_coll_test_logger: RootLogger,
    test_db_url:str,
) -> None:
    """Test for pushing to database table where 'today' data already exists"""
    list_df_name_today_exists = [
        f"{df_name}_today_exists" for df_name in df_dict_test.keys()
    ]

    with sqlalchemy.create_engine(test_db_url).connect() as db_conn:
        for df_name_today,df_name_og in \
            zip(list_df_name_today_exists, df_dict_test.keys()):

            df_dict_test[df_name_og].to_sql(
                name=df_name_today,
                con=db_conn,
                if_exists='append',
                index=False
            )

        with pytest.raises(TodayDataAlreadyExistsError):
            push_to_db(db_conn,gpu_data_coll_test_logger,**df_dict_test)
