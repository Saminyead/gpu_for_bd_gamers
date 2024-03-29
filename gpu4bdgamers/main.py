import os
from dotenv import load_dotenv

from gpu4bdgamers.data_coll_script import (
    data_collection_to_df, data_collection_to_db
)

def main() -> None:
    load_dotenv()
    db_url = os.getenv("db_url_new")

    df_dict = data_collection_to_df()

    df_dict_to_append = {
        "gpu_of_interest": df_dict['gpu_of_interest'],
        "lowest_prices" : df_dict['lowest_prices'],
    }

    df_dict_to_replace = {
        "lowest_prices_tiered": df_dict['lowest_prices_tiered']
    }

    data_collection_to_db(
        db_url,
        df_dict_to_append,
        df_dict_to_replace
    )

if __name__=="__main__":
    main()