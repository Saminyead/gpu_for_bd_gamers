from logging import RootLogger
import os
from dotenv import load_dotenv

import re

import pandas as pd

from gpu4bdgamers.data_coll_funcs import *

import sqlalchemy

from functools import partial

import math

from gpu4bdgamers.logger import setup_logging
from gpu4bdgamers.overall_tier_score import df_overall_tier_score
from gpu4bdgamers.database import push_to_db, replace_previous_date_data_table_db
from gpu4bdgamers.gpu_units import add_gpu_unit_name

import pathlib


def read_gpu_from_files(filename:str|pathlib.Path) -> list[str]:
    with open(filename,'r') as gpu_reader:
        gpu_unit_text = gpu_reader.read()
        gpu_unit_list = gpu_unit_text.splitlines()
        if "" in gpu_unit_list:
            gpu_unit_list.remove('')
        return gpu_unit_list


def get_master_df(
        first_pg_links:dict[str,str],
        card_css_selectors:dict[str,str],
        logger:RootLogger
) -> pd.DataFrame:
    #--scraping through all the websites

    # Ryan's Computer
    ryans_pages = get_pages_find_all(first_pg_link=first_pg_links['ryans'],url_tag_str='›')['soup_list']

    ryans_card_list = get_card_list(
        pages_list=ryans_pages,
        card_css_selector=card_css_selectors['ryans']
    )

    ryans_df = gpu_dataframe_card(
        card_list=ryans_card_list,
        gpu_name_css_sel='p.card-text.p-0.m-0.grid-view-text > a',
        gpu_price_css_sel='a.pr-text.cat-sp-text.pb-1',
        retailer_name='Ryans Computer'
    )

    logger.info(msg=f'Ryans Computer BD data scraped and stored to a dataframe successfully; length of dataframe = {len(ryans_df)}')


    # Startech Engineering
    startech_pages = get_pages_find_all(first_pg_link=first_pg_links['startech'],url_tag_str='NEXT')['soup_list']

    startech_card_list = get_card_list(
        pages_list=startech_pages,
        card_css_selector=card_css_selectors['startech']
    )

    startech_df = gpu_dataframe_card(
        card_list=startech_card_list,
        gpu_name_css_sel='h4.p-item-name > a',
        gpu_price_css_sel='div.p-item-price > span',
        retailer_name='Startech Engineering'
    )

    logger.info(msg=f'Startech Engineering BD data scraped and stored to a dataframe successfully; length of dataframe = {len(startech_df)}')


    # Techland BD
    techlandbd_pages = get_pages_find_all(first_pg_link=first_pg_links['techlandbd'],url_tag_str='>')['soup_list']

    techlandbd_card_list = get_card_list(
        pages_list=techlandbd_pages,
        card_css_selector=card_css_selectors['techlandbd']
    )

    techlandbd_df = gpu_dataframe_card(
        card_list=techlandbd_card_list,
        gpu_name_css_sel='div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='Tech Land BD'
    )

    logger.info(msg=f'Tech Land BD data scraped and stored to a dataframe successfully; length of dataframe = {len(techlandbd_df)}')


    # Skyland Computer BD
    skyland_pages = get_pages_select(first_pg_link=first_pg_links['skyland'],css_selector='a.next.page-number')['soup_list']

    skyland_card_list = get_card_list(
        pages_list=skyland_pages,
        card_css_selector=card_css_selectors['skyland']
    )

    skyland_df = gpu_dataframe_card(
        card_list=skyland_card_list,
        gpu_name_css_sel='div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='Skyland Computer Bd'
    )

    logger.info(msg=f'Skyland Computer BD data scraped and stored to a dataframe successfully; length of dataframe = {len(skyland_df)}')

    # Ultra Technology BD
    ultratech_pages = get_pages_select(
        first_pg_link=first_pg_links['ultratech'],
        css_selector='a.next')['soup_list']

    ultratech_card_list = get_card_list(
        pages_list=ultratech_pages,
        card_css_selector=card_css_selectors['ultratech']
    )

    ultratech_df_0 = gpu_dataframe_card(
        card_list=ultratech_card_list,
        gpu_name_css_sel='div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='Ultra Technology'
    )

    # since some of the products that are currently not in stock are marked as BDT. 0 in the html code
    ultratech_df = ultratech_df_0.loc[ultratech_df_0['gpu_price']!=0]

    logger.info(msg=f'Ultra Technology data scraped and stored to a dataframe successfully; length of dataframe = {len(ultratech_df)}')

    # Nexus Computer Bangladesh
    nexusbd_pages = get_pages_select_pagination(
        first_pg_link=first_pg_links['nexusbd'],
        css_selector='div#pagination_block_bottom > div.ty-pagination__items ~ a')['soup_list']

    nexusbd_card_list = get_card_list(
        pages_list=nexusbd_pages,
        card_css_selector=card_css_selectors['nexusbd']
    )

    nexusbd_df = gpu_dataframe_card(
        card_list=nexusbd_card_list,
        gpu_name_css_sel='h2 > a.product-title',
        gpu_price_css_sel='span.ty-price > bdi > span ~ span',
        retailer_name='Nexus Technology'
    )

    logger.info(msg=f'Nexus Technology data scraped and stored to a dataframe successfully; length of dataframe = {len(nexusbd_df)}')

    # Global Brand
    # Global Brand only has a single page
    globalbrand_pages = get_pages_single_page(first_pg_links['globalbrand'])['soup_list']

    globalbrand_card_list = get_card_list(
        pages_list=globalbrand_pages,
        card_css_selector=card_css_selectors['globalbrand']
    )

    # the following dataframe contains rows of '0 price', basically they are the unavailable ones. Thus, filterting them out into a new dataframe
    globalbrand_df_0 = gpu_dataframe_card(
        card_list=globalbrand_card_list,
        gpu_name_css_sel='div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='Global Brand'
    )

    globalbrand_df = globalbrand_df_0.loc[globalbrand_df_0['gpu_price']!=0]

    logger.info(msg=f'Global Brand data scraped and stored to a dataframe successfully; length of dataframe = {len(globalbrand_df)}')

    # Creatus Computer 
    creatus_pages = get_pages_select(
        first_pg_link=first_pg_links['creatus'],
        css_selector='li > a.next')['soup_list']

    creatus_card_list = get_card_list(
        pages_list=creatus_pages,
        card_css_selector=card_css_selectors['creatus']
    )

    creatus_df = gpu_dataframe_card(
        card_list=creatus_card_list,
        gpu_name_css_sel='div.caption > div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='Creatus Computer'
    )


    while True:
        if len(creatus_df) > 0:
            break

        else:
            creatus_df = retry_with_scraperapi_pages_select(
                scraperapi_api_key=os.getenv("scraperapi_api_key"),
                first_pg_link=first_pg_links['creatus'],
                pages_css_selector='li > a.next',
                card_css_selector=card_css_selectors['creatus'],
                gpu_name_css_sel='div.caption > div.name > a',
                gpu_price_css_sel='div.price > div > span',
                retailer_name='Creatus Computer'
            )

    logger.info(msg=f'Cretaus Computer data scraped and stored to a dataframe successfully; length of dataframe = {len(creatus_df)}')

    # UCC BD
    uccbd_pages = get_pages_single_page(first_pg_links['uccbd'])['soup_list']

    uccbd_card_list = get_card_list(
        pages_list=uccbd_pages,
        card_css_selector=card_css_selectors['uccbd']
    )

    uccbd_df = gpu_dataframe_card(
        card_list=uccbd_card_list,
        gpu_name_css_sel='div.caption > div.name > a',
        gpu_price_css_sel='div.price > div > span',
        retailer_name='UCC-BD'
    )

    logger.info(msg=f'UCC-BD data scraped and stored to a dataframe successfully; length of dataframe = {len(uccbd_df)}')

    list_of_df = [ryans_df,startech_df,techlandbd_df,skyland_df,ultratech_df,nexusbd_df,globalbrand_df,creatus_df,uccbd_df]
    master_df = pd.concat(list_of_df)

    logger.info(msg=f'All dataframes compiled into master_df of length {len(master_df)}')
    logger.info(msg=f'Number of retailers in master df is {len(master_df.retailer_name.unique())}, while length of list_of_df is {len(list_of_df)}')

    # any row which has a GPU price of 0 should be discarded
    master_df = master_df.loc[master_df.gpu_price!=0]

    return master_df


def data_collection_to_df(
        master_df:pd.DataFrame,
        geforce_gpu_units_filepath:pathlib.Path,
        radeon_gpu_units_filepath:pathlib.Path,
        intel_gpu_units_filepath:pathlib.Path,
        logger:RootLogger
) -> dict[str,pd.DataFrame]:
    
    # rounding the GPU Prices to their nearest hundreds

    master_df['gpu_price']=master_df['gpu_price'].apply(lambda x: 100 * math.ceil(x/100))

    # list of all gpu units of interest
    geforce_gpu_unit_list = read_gpu_from_files(
        geforce_gpu_units_filepath
    )

    logger.info(msg='Added list of Geforce GPUs from file')

    radeon_gpu_unit_list = read_gpu_from_files(
        radeon_gpu_units_filepath
    )

    logger.info(msg='Added list of Radeon GPUs from file')

    intel_gpu_unit_list = read_gpu_from_files(
        intel_gpu_units_filepath
    )

    logger.info(msg='Added list of Intel GPUs from file')

    logger.info(msg=f'Total number of GPUs = {len(geforce_gpu_unit_list+radeon_gpu_unit_list+intel_gpu_unit_list)}')


    # all geforce gpu's
    geforce_gpu_df = add_gpu_unit_name(master_df,geforce_gpu_unit_list,'Geforce')
    geforce_gpu_df.reset_index(drop=True,inplace=True)

    # GTX 1050 Ti are written in varying formats across websites (e.g. GTX 1050ti, GTX 1050 Ti, GTX1050Ti)
    # and there are no GTX 1050's available, so it is just easier to make a separate dataframe for it
    df_1050_ti = master_df.loc[master_df['gpu_name'].str.contains('1050')].copy()
    df_1050_ti['gpu_unit_name'] = 'Geforce GTX 1050 Ti'

    def gddr5_vs_gddr6_1650(gpu_1650):
        """since there are both gddr5 and gddr6 versions of the GTX 1650 with significant performance difference,
        this function distinguishes between them (to be applied with the .apply() method in dataframe)
        Args:
            gpu_1650 (string): GTX 1650 gpu name (as listed on retailer website)
        Returns:
            string: "GTX 1650 GDDR6"/"GTX 1650 GDDR5"
        """
        # sometimes the retailer names have the full 'GDDR6'/'GDDR5' spelled out, sometimes it just has 'D6'/'D5' in the name
        regex_match = re.search(pattern='gddr6|d6',string=gpu_1650,flags=re.I)
        if bool(regex_match) == True:
            return 'Geforce GTX 1650 GDDR6'
        else:
            return 'Geforce GTX 1650 GDDR5'



    rtx_3080_10_vs_12 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3080",
        pattern_version_dict={'12gb|12g':'12GB','10gb|10g':'10GB'}
    )

        
    rtx_3060_8_vs_12 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3060",
        pattern_version_dict={'12gb|12g':'12GB','8gb|8g':'8GB'}
    )


    rtx_3050_6_vs_8 = partial(
        gpu_version_diff,
        gpu_name="Geforce RTX 3050",
        pattern_version_dict={'6gb|6g':'6GB','8gb|8g':'8GB'}
    )

    geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce GTX 1650','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(gddr5_vs_gddr6_1650)
    geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce RTX 3080','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(rtx_3080_10_vs_12)
    geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce RTX 3060','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(rtx_3060_8_vs_12)
    
    geforce_gpu_df.loc[
        geforce_gpu_df['gpu_unit_name']=='Geforce RTX 3050','gpu_unit_name'
    ] = geforce_gpu_df['gpu_name'].apply(rtx_3050_6_vs_8)


    # all radeon and intel gpu's
    radeon_gpu_df = add_gpu_unit_name(master_df,radeon_gpu_unit_list,'Radeon')
    radeon_gpu_df.reset_index(drop=True,inplace=True)

    rx_580_4gb_vs_8gb = partial(
        gpu_version_diff,
        gpu_name="Radeon RX 580",
        pattern_version_dict={"8gb|8g":"8GB","4gb|4g":"4GB"}
    )

    radeon_gpu_df.loc[radeon_gpu_df.gpu_unit_name=="Radeon RX 580",'gpu_unit_name'] = radeon_gpu_df['gpu_name'].apply(rx_580_4gb_vs_8gb)

    intel_arc_gpu_df = add_gpu_unit_name(master_df,intel_gpu_unit_list,'Intel')
    intel_arc_gpu_df.reset_index(drop=True,inplace=True)

    arc_a770_8_vs_16 = partial(
        gpu_version_diff,
        gpu_name="Intel Arc A770",
        pattern_version_dict={"8gb|8g":"8GB","16gb|16g":"16GB"}
    )

    intel_arc_gpu_df.loc[
        intel_arc_gpu_df['gpu_unit_name']=='Intel Arc A770','gpu_unit_name'
    ] = intel_arc_gpu_df['gpu_name'].apply(arc_a770_8_vs_16)

    # all graphics cards of interest
    gpu_of_interest_df = pd.concat([geforce_gpu_df,radeon_gpu_df,intel_arc_gpu_df,df_1050_ti])
    gpu_of_interest_df.reset_index(drop=True,inplace=True)

    logger.info(f'gpu_of_interest_df created with {len(gpu_of_interest_df)} entries')

    lowest_price_df=gpu_of_interest_df[gpu_of_interest_df['gpu_price'] == gpu_of_interest_df.groupby('gpu_unit_name')['gpu_price'].transform(min)]
    lowest_price_df.reset_index(drop=True,inplace=True)

    logger.info(f'lowest_price_df created with {len(lowest_price_df)} entries')

    overall_tier_score_df = df_overall_tier_score()

    lowest_prices_tiered=pd.merge(
        left=lowest_price_df,
        right=overall_tier_score_df[['gpu_unit_name','base_tier_score', 'net_tier_score', 'non_rt_net_score']],
        on='gpu_unit_name'
        )

    logger.info(f'lowest_prices_tiered dataframe created with {len(lowest_prices_tiered)} rows and {len(lowest_prices_tiered.columns)} column')

    # adding price per tier score columns to dataframe

    lowest_prices_tiered['price_per_base_tier'] = lowest_prices_tiered['gpu_price']/lowest_prices_tiered['base_tier_score']
    lowest_prices_tiered['price_per_net_tier'] = lowest_prices_tiered.gpu_price/lowest_prices_tiered.net_tier_score
    lowest_prices_tiered['price_per_non_rt_tier'] = lowest_prices_tiered.gpu_price/lowest_prices_tiered.non_rt_net_score

    logger.info(
        f'3 columns added to lowest_prices_tiered dataframe being {lowest_prices_tiered.columns[-3]}, {lowest_prices_tiered.columns[-2]} and {lowest_prices_tiered.columns[-1]}')
    
    return {
            "gpu_of_interest" : gpu_of_interest_df,
            "lowest_prices" : lowest_price_df,
            "lowest_prices_tiered" : lowest_prices_tiered
    }




def data_collection_to_db(
        db_url:str,
        df_table_to_append_dict: dict[str,pd.DataFrame],
        df_table_to_replace_dict: dict[str,pd.DataFrame],
        logger:RootLogger
) -> None:
    """The main function containing all the code. 
    For now, will take the following arg:

    db_url(str): the database url where the gpu data will be pushed."""

    conn = sqlalchemy.create_engine(db_url).connect()
    push_to_db(
        conn=conn,
        logger=logger,
        **df_table_to_append_dict
    )

    replace_previous_date_data_table_db(
        conn=conn,
        logger=logger,
        **df_table_to_replace_dict
    )
