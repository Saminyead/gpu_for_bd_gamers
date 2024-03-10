import sqlalchemy
import pandas as pd

from datetime import date

from gpu4bdgamers.logger import setup_logging


class TodayDataAlreadyExistsError(Exception):
    def __init__(self, table_name:str) -> None:
        super().__init__(f"Today's data already exists in {table_name}")


def _check_if_today_data_exists(
        conn:sqlalchemy.engine.base.Connection,
        table_name:str,
) -> bool:
    today = date.today().strftime("%Y-%m-%d")
    df_sql_table = pd.read_sql(
        sql=f"SELECT * FROM {table_name} WHERE data_collection_date = '{today}'",
        con=conn,        
    )

    if len(df_sql_table) == 0:
        return True     # it means doesn't exist, we can write to table
    
    else:
        raise TodayDataAlreadyExistsError(table_name)


def push_to_db(
        conn:sqlalchemy.engine.base.Connection,
        **df_kwargs:pd.DataFrame
) -> None:
    """Pushes dataframe to database

    Args:
        conn (sqlalchemy.engine.base.Connection): the sqlalchemy 
        connection object
        
        **df_kwargs (pd.DataFrame): a dictionary of dataframes as 
        keyword arguments
    """
    logging = setup_logging()

    logging.info(msg='Connection to database established')

    for table_name,df in df_kwargs.items():
        _check_if_today_data_exists(conn,table_name)

        # TODO: if the check raises error, skip the table

        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
        

    logging.info(f"Data appended to table {table_name};\
                 number of rows = {len(df)}")
    



def replace_previous_date_data_table_db(
        conn:sqlalchemy.engine.base.Connection,
        **df_kwargs:pd.DataFrame
) -> None:
    """Replace previous date's data with today's data (esp. for 
    lowest_prices_tiered_sqlalchemy)

    Args:
        conn (sqlalchemy.engine.base.Connection): the sqlalchemy 
        connection object

        **df_kwargs (pd.DataFrame): dataframes as keyword arguments (
        so that dataframe data can be pushed to table)
    """
    logging = setup_logging()
    push_to_db(conn,**df_kwargs)

    for table_name, df in df_kwargs.items():
        # deleting all rows written before today
        today = date.today().strftime('%Y-%m-%d')
        metadata = sqlalchemy.MetaData()
        db_table = sqlalchemy.Table(
            table_name,
            metadata,
            sqlalchemy.Column('retail_url',sqlalchemy.String,primary_key=True),
            sqlalchemy.Column('data_collection_date',sqlalchemy.String)
        )
        
        delete_previous_date_data = db_table.delete().\
            where(db_table.c.data_collection_date!=today)
        conn.execute(delete_previous_date_data)
        logging.info(msg= 'Data of previous dates deleted.')

        logging.info(msg=f'All dataframes written to database for {today}\n')