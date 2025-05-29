import os
from dotenv import load_dotenv

from gpu4bdgamers.run import data_collection_to_df, data_collection_to_db, get_master_df

from gpu4bdgamers.dirs import (
    SCRAPING_CONFIG_FILE,
    GEFORCE_UNITS_FILE,
    RADEON_UNITS_FILE,
    INTEL_UNITS_FILE,
    GPU_DATA_EXCEL_FILE,
)

from gpu4bdgamers.logger import setup_logging
from gpu4bdgamers.dirs import LOGS_DIR


def main() -> None:
    load_dotenv()
    db_url = os.getenv("db_url_new")

    LOGGER = setup_logging(log_dir=LOGS_DIR, log_filename="gpu_data_coll_script.log")

    master_df = get_master_df(SCRAPING_CONFIG_FILE, LOGGER)

    df_dict = data_collection_to_df(
        master_df,
        GEFORCE_UNITS_FILE,
        RADEON_UNITS_FILE,
        INTEL_UNITS_FILE,
        LOGGER,
        GPU_DATA_EXCEL_FILE,
    )

    df_dict_to_append = {
        "gpu_of_interest": df_dict["gpu_of_interest"],
        "lowest_prices": df_dict["lowest_prices"],
    }

    df_dict_to_replace = {"lowest_prices_tiered": df_dict["lowest_prices_tiered"]}

    data_collection_to_db(db_url, df_dict_to_append, df_dict_to_replace, LOGGER)


if __name__ == "__main__":
    main()
