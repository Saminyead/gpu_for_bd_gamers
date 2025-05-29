from logging import RootLogger, Logger


import pandas as pd

import sqlalchemy

from functools import partial

import math

from gpu4bdgamers.overall_tier_score import df_overall_tier_score
from gpu4bdgamers.database import push_to_db, replace_previous_date_data_table_db
from gpu4bdgamers.naming import add_gpu_unit_name, gddr5_vs_gddr6_1650, gpu_version_diff

from gpu4bdgamers.scraping import (
    get_page_soup_list,
    get_card_list,
    retry_with_scraperapi,
    GpuListingAttrs,
    GpuListingData,
    ElementDoesNotExistError,
)
import toml
from datetime import datetime

import pathlib

def get_master_df(
    scraping_config_file: str | pathlib.Path,
    logger: Logger,
    scraperapi_api_key: str | None = None,
):
    toml_content = toml.load(scraping_config_file)
    first_page_url_dict = toml_content["first_page_urls"]
    card_sel_dict = toml_content["card_sels"]
    next_page_url_sel_dict = toml_content["next_page_url_sels"]
    gpu_listing_attributes_dict = toml_content["gpu_listing_attrs"]
    retailer_keyword_list = [key for key in first_page_url_dict.keys()]
    all_gpu_listing_data = []

    for retailer in retailer_keyword_list:
        first_page_url = first_page_url_dict[retailer]
        next_page_url = None
        if retailer in next_page_url_sel_dict.keys():
            next_page_url = next_page_url_sel_dict[retailer]
        card_css_sel = card_sel_dict[retailer]
        gpu_listing_attrs_retailer = gpu_listing_attributes_dict[retailer]
        gpu_listing_attrs = GpuListingAttrs(**gpu_listing_attrs_retailer)
        page_soup_list = get_page_soup_list(first_page_url, next_page_url)
        logger.info(f"Number of pages for {retailer} = {len(page_soup_list)}")
        try:
            card_list = get_card_list(page_soup_list, card_css_sel)
            logger.info(f"Number of cards for {retailer} = {len(card_list)}")
        except ElementDoesNotExistError:
            page_soup_list = get_page_soup_list(
                first_page_url,
                next_page_url,
                request_func=retry_with_scraperapi,
                scraperapi_api_key=scraperapi_api_key,
            )
            logger.info(
                f"Number of pages after retrying with scraperapi for {retailer} = {len(page_soup_list)}"
            )
            card_list = get_card_list(page_soup_list, card_css_sel)
            logger.info(
                f"Number of cards after retrying with scraperapi for {retailer} = {len(card_list)}"
            )
        gpu_listing_data = gpu_listing_attrs.get_gpu_listing_data(card_list)
        all_gpu_listing_data.extend(gpu_listing_data)
        logger.info(
            f"Total number of gpu's found for {retailer} = {len(gpu_listing_data)}"
        )

    all_gpu_listing_data_dict = [
        gpu_listing_data.model_dump() for gpu_listing_data in all_gpu_listing_data
    ]
    df = create_df_from_gpu_listing_data(all_gpu_listing_data_dict)
    logger.info(f"master_df len = {len(df)}")
    return df


def create_df_from_gpu_listing_data(
    gpu_listing_data_dict_list: list[dict],
    date_col_pos: int = 3,
    date_col_name="data_collection_date",
) -> pd.DataFrame:
    df = pd.DataFrame(gpu_listing_data_dict_list)
    # needs to be converted to string from AnyUrl for compatibility with database
    df["retail_url"] = df["retail_url"].apply(lambda x: str(x))
    date_col = [datetime.today().strftime("%Y-%m-%d")] * len(df)
    df.insert(loc=date_col_pos, column=date_col_name, value=date_col)
    return df

def read_gpu_from_files(filename: str | pathlib.Path) -> list[str]:
    with open(filename, "r") as gpu_reader:
        gpu_unit_text = gpu_reader.read()
        gpu_unit_list = gpu_unit_text.splitlines()
        if "" in gpu_unit_list:
            gpu_unit_list.remove("")
        return gpu_unit_list


def get_gpu_of_interest_df(
    master_df: pd.DataFrame,
    geforce_gpu_units_filepath: str | pathlib.Path,
    radeon_gpu_units_filepath: str | pathlib.Path,
    intel_gpu_units_filepath: str | pathlib.Path,
    logger: RootLogger,
):
    master_df["gpu_price"] = master_df["gpu_price"].apply(
        lambda x: 100 * math.ceil(x / 100)
    )

    # list of all gpu units of interest
    geforce_gpu_unit_list = read_gpu_from_files(geforce_gpu_units_filepath)
    logger.info(msg="Added list of Geforce GPUs from file")

    radeon_gpu_unit_list = read_gpu_from_files(radeon_gpu_units_filepath)
    logger.info(msg="Added list of Radeon GPUs from file")

    intel_gpu_unit_list = read_gpu_from_files(intel_gpu_units_filepath)
    logger.info(msg="Added list of Intel GPUs from file")

    logger.info(
        msg=f"Total number of GPUs = {len(geforce_gpu_unit_list+radeon_gpu_unit_list+intel_gpu_unit_list)}"
    )

    # all geforce gpu's
    geforce_gpu_df = add_gpu_unit_name(master_df, geforce_gpu_unit_list, "Geforce")
    geforce_gpu_df.reset_index(drop=True, inplace=True)
    rtx_3080_10_vs_12 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3080",
        pattern_version_dict={"12gb|12g": "12GB", "10gb|10g": "10GB"},
    )
    rtx_3060_8_vs_12 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3060",
        pattern_version_dict={"12gb|12g": "12GB", "8gb|8g": "8GB"},
    )
    rtx_3050_6_vs_8 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3050",
        pattern_version_dict={"6gb|6g": "6GB", "8gb|8g": "8GB"},
    )

    geforce_gpu_df.loc[
        geforce_gpu_df["gpu_unit_name"] == "Geforce GTX 1650", "gpu_unit_name"
    ] = geforce_gpu_df["gpu_name"].apply(gddr5_vs_gddr6_1650)
    geforce_gpu_df.loc[
        geforce_gpu_df["gpu_unit_name"] == "Geforce RTX 3080", "gpu_unit_name"
    ] = geforce_gpu_df["gpu_name"].apply(rtx_3080_10_vs_12)
    geforce_gpu_df.loc[
        geforce_gpu_df["gpu_unit_name"] == "Geforce RTX 3060", "gpu_unit_name"
    ] = geforce_gpu_df["gpu_name"].apply(rtx_3060_8_vs_12)
    geforce_gpu_df.loc[
        geforce_gpu_df["gpu_unit_name"] == "Geforce RTX 3050", "gpu_unit_name"
    ] = geforce_gpu_df["gpu_name"].apply(rtx_3050_6_vs_8)

    # all radeon and intel gpu's
    radeon_gpu_df = add_gpu_unit_name(master_df, radeon_gpu_unit_list, "Radeon")
    radeon_gpu_df.reset_index(drop=True, inplace=True)

    rx_580_4gb_vs_8gb = partial(
        gpu_version_diff,
        gpu_name="Radeon RX 580",
        pattern_version_dict={"8gb|8g": "8GB", "4gb|4g": "4GB"},
    )

    radeon_gpu_df.loc[
        radeon_gpu_df.gpu_unit_name == "Radeon RX 580", "gpu_unit_name"
    ] = radeon_gpu_df["gpu_name"].apply(rx_580_4gb_vs_8gb)

    intel_arc_gpu_df = add_gpu_unit_name(master_df, intel_gpu_unit_list, "Intel")
    intel_arc_gpu_df.reset_index(drop=True, inplace=True)

    arc_a770_8_vs_16 = partial(
        gpu_version_diff,
        gpu_name="Intel Arc A770",
        pattern_version_dict={"8gb|8g": "8GB", "16gb|16g": "16GB"},
    )

    intel_arc_gpu_df.loc[
        intel_arc_gpu_df["gpu_unit_name"] == "Intel Arc A770", "gpu_unit_name"
    ] = intel_arc_gpu_df["gpu_name"].apply(arc_a770_8_vs_16)

    # all graphics cards of interest
    gpu_of_interest_df = pd.concat([geforce_gpu_df, radeon_gpu_df, intel_arc_gpu_df])
    gpu_of_interest_df.reset_index(drop=True, inplace=True)

    logger.info(f"gpu_of_interest_df created with {len(gpu_of_interest_df)} entries")
    return gpu_of_interest_df


def data_collection_to_df(
    master_df: pd.DataFrame,
    geforce_gpu_units_filepath: pathlib.Path,
    radeon_gpu_units_filepath: pathlib.Path,
    intel_gpu_units_filepath: pathlib.Path,
    logger: RootLogger,
    tier_score_excel_file: pathlib.Path,
) -> dict[str, pd.DataFrame]:
    """Top level function to clean and properly format master_df, and proper
    naming and prefixes, and finally returns dataframes to be pushed to
    database.

    Returns a dictionary of dataframes as values:
        {
            'gpu_of_interest': gpu_of_interest,
            'lowest_prices': lowest_prices,
            'lowest_prices_tiered': lowest_prices_tiered
        }
    """
    gpu_of_interest_df = get_gpu_of_interest_df(
        master_df,
        geforce_gpu_units_filepath,
        radeon_gpu_units_filepath,
        intel_gpu_units_filepath,
        logger,
    )
    lowest_price_df = gpu_of_interest_df[
        gpu_of_interest_df["gpu_price"]
        == gpu_of_interest_df.groupby("gpu_unit_name")["gpu_price"].transform(min)
    ]
    lowest_price_df.reset_index(drop=True, inplace=True)
    logger.info(f"lowest_price_df created with {len(lowest_price_df)} entries")
    overall_tier_score_df = df_overall_tier_score(logger, tier_score_excel_file)
    lowest_prices_tiered = pd.merge(
        left=lowest_price_df,
        right=overall_tier_score_df[
            ["gpu_unit_name", "base_tier_score", "net_tier_score", "non_rt_net_score"]
        ],
        on="gpu_unit_name",
    )
    logger.info(
        f"lowest_prices_tiered dataframe created with {len(lowest_prices_tiered)} rows and {len(lowest_prices_tiered.columns)} column"
    )
    # adding price per tier score columns to dataframe
    lowest_prices_tiered["price_per_base_tier"] = (
        lowest_prices_tiered["gpu_price"] / lowest_prices_tiered["base_tier_score"]
    )
    lowest_prices_tiered["price_per_net_tier"] = (
        lowest_prices_tiered.gpu_price / lowest_prices_tiered.net_tier_score
    )
    lowest_prices_tiered["price_per_non_rt_tier"] = (
        lowest_prices_tiered.gpu_price / lowest_prices_tiered.non_rt_net_score
    )

    logger.info(
        f"3 columns added to lowest_prices_tiered dataframe being {lowest_prices_tiered.columns[-3]}, {lowest_prices_tiered.columns[-2]} and {lowest_prices_tiered.columns[-1]}"
    )

    return {
        "gpu_of_interest": gpu_of_interest_df,
        "lowest_prices": lowest_price_df,
        "lowest_prices_tiered": lowest_prices_tiered,
    }


def data_collection_to_db(
    db_url: str,
    df_table_to_append_dict: dict[str, pd.DataFrame],
    df_table_to_replace_dict: dict[str, pd.DataFrame],
    logger: RootLogger,
) -> None:
    """The main function containing all the code.
    For now, will take the following arg:

    db_url(str): the database url where the gpu data will be pushed."""

    conn = sqlalchemy.create_engine(db_url).connect()
    push_to_db(conn=conn, logger=logger, **df_table_to_append_dict)

    replace_previous_date_data_table_db(
        conn=conn, logger=logger, **df_table_to_replace_dict
    )
