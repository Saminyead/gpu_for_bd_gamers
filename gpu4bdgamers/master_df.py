from gpu4bdgamers.scraping import (
    get_page_soup_list,
    get_card_list,
    retry_with_scraperapi,
    GpuListingAttrs,
    GpuListingData,
    ElementDoesNotExistError,
)
import pandas as pd
from datetime import datetime
import toml
from pathlib import Path
from logging import Logger


def get_master_df(
    scraping_config_file: str | Path,
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
