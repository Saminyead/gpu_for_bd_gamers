import sqlalchemy
import pandas as pd

from datetime import date

from logger import setup_logging

def push_to_db(
        db_url:str,
        **df_kwargs:pd.DataFrame
) -> None:
    """Pushes dataframe to database

    Args:
        db_url (str): the database connection url
        
        **df_kwargs (pd.DataFrame): a dictionary of dataframes as 
        keyword arguments
    """
    logging = setup_logging()

    pgsql_db_engine = sqlalchemy.create_engine(db_url).connect()
    logging.info(msg='Connection to database established')

    for table_name,df in df_kwargs.items():
        df.to_sql(
            name=table_name,
            con=pgsql_db_engine,
            if_exists='append',
            index=False
        )

    logging.info(f"Data appended to table {table_name};\
                 number of rows = {len(df)}")
    



def delete_table_from_db(
        conn:sqlalchemy.engine.base.Connection,
) -> None:
    logging = setup_logging()
    # deleting all rows written before today
    today = date.today().strftime('%Y-%m-%d')
    metadata = sqlalchemy.MetaData()
    lowest_prices_tiered_sqlalchemy = sqlalchemy.Table(
        "lowest_prices_tiered",
        metadata,
        sqlalchemy.Column('retail_url',sqlalchemy.String,primary_key=True),
        sqlalchemy.Column('data_collection_date',sqlalchemy.String)
    )
    
    delete_previous_date_data = lowest_prices_tiered_sqlalchemy.delete().\
        where(lowest_prices_tiered_sqlalchemy.c.data_collection_date!=today)
    conn.execute(delete_previous_date_data)
    logging.info(msg= 'Data of previous dates deleted.')

    logging.info(msg=f'All dataframes written to database for {today}\n')