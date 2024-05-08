import os
from dotenv import load_dotenv

from gpu4bdgamers.data_coll_script import (
    get_master_df,data_collection_to_df, data_collection_to_db
)

import toml
from gpu4bdgamers.dirs import SCRAPING_CONFIG_FILE

def main() -> None:
    load_dotenv()
    db_url = os.getenv("db_url_new")

    # --constants
    with open(SCRAPING_CONFIG_FILE,'r') as f:
        SCRAPING_CONFIG_CONTENTS = toml.load(f)

    FIRST_PAGES:dict[str,str] = SCRAPING_CONFIG_CONTENTS['first_page_urls']
    CARD_CSS_SELECTORS:dict[str,str] = SCRAPING_CONFIG_CONTENTS['card_css_selectors']

    master_df = get_master_df(
        first_pg_links=FIRST_PAGES,
        card_css_selectors=CARD_CSS_SELECTORS
    )

    df_dict = data_collection_to_df(master_df)

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