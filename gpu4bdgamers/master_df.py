from gpu4bdgamers.scraping import get_page_soup_list, get_card_list, GpuListingAttrs
import toml
from pathlib import Path

def get_master_df(scraping_config_file: str|Path):
    toml_content = toml.load(scraping_config_file)
    first_page_url_dict = toml_content['first_page_urls']
    card_sel_dict = toml_content['card_sels']
    retailer_keyword_list = [key for key,_ in first_page_url_dict]
    gpu_listing_attributes_dict = toml_content['gpu_listing_attrs']

    for retailer in retailer_keyword_list:
        retailer_listing = gpu_listing_attributes_dict[retailer]
