from data_coll_script import main

import os
import dotenv

import pandas as pd
import datetime
import sqlalchemy

dotenv.load_dotenv("test.env")
test_db_url = os.getenv("test_db_url")

def sql_query_format(table_name:str):
    """formats the sql query so we can just plug in table_name 
    in test_main"""
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    return f"SELECT * FROM {table_name} WHERE data_collection_date = '{today}'"


def test_main(
        test_db_url:str = test_db_url
    ):
    """Directly tests main on a test database"""

    main(test_db_url)

    db_conn = sqlalchemy.create_engine(test_db_url).connect()

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