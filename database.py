import sqlalchemy
import pandas as pd

from logger import setup_logging

def push_to_db(
        db_url:str,
        **df_dict:dict[pd.DataFrame]
) -> None:
    """Pushes dataframe to database

    Args:
        db_url (str): the database connection url
        
        **df_dict (dict[pd.DataFrame]): a dictionary of dataframes as 
        keyword arguments
    """
    logging = setup_logging()

    pgsql_db_engine = sqlalchemy.create_engine(db_url).connect()
    logging.info(msg='Connection to database established')

    for table_name,df in df_dict.items():
        df.to_sql(
            name=table_name,
            con=pgsql_db_engine,
            if_exists='append',
            index=False
        )

    logging.info(f"Data appended to table {table_name};\
                 number of rows = {len(df)}")
    



def delete_table_from_db(db_url:str,**kwargs):
    # deleting all rows written before today
    today = date.today().strftime('%Y-%m-%d')
    metadata = MetaData()
    lowest_prices_tiered_sqlalchemy = Table(
        "lowest_prices_tiered",metadata,
        Column('retail_url',String,primary_key=True),
        Column('data_collection_date',String)
    )
    delete_previous_date_data = lowest_prices_tiered_sqlalchemy.delete().where(lowest_prices_tiered_sqlalchemy.c.data_collection_date!=today)
    pgsql_db_engine.connect().execute(delete_previous_date_data)
    logging.info(msg= 'Data of previous dates deleted.')

    logging.info(msg=f'All dataframes written to database for {today}\n')