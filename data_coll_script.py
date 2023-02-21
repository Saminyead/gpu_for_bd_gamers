import os
import pandas as pd
import re
from bs4 import BeautifulSoup as bsoup
from openpyxl import load_workbook
import sqlalchemy
from data_coll_funcs import *
import logging
from dotenv import load_dotenv


#--setting up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("./logs/gpu_data_coll_script.log"),
        logging.StreamHandler()
    ]
)



#--scraping through all the websites

# Ryan's Computer
ryans_pages = get_pages(first_pg_link='https://www.ryanscomputers.com/category/desktop-component-graphics-card?sort=LH&osp=0&page=1',
                        url_tag_tag='a',
                        url_tag_str='›')['soup_list']
ryans_card_list = get_card_list(pages_list=ryans_pages,card_tag='div.card-body.text-center')
ryans_df = gpu_dataframe_card(card_list=ryans_card_list,gpu_name_tag='p.card-text.p-0.m-0.list-view-text > a',
                                gpu_price_tag='div.short-desc-attr ~ p',retailer_name='Ryans Computer')

logging.info(msg=f'\nRyans Computer BD data scraped and stored to a dataframe successfully; length of dataframe = {len(ryans_df)}')

# Startech Engineering
startech_pages = get_pages(first_pg_link='https://www.startech.com.bd/component/graphics-card?filter_status=7&sort=p.price&order=ASC',
                        url_tag_tag='a',
                        url_tag_str='NEXT')['soup_list']
startech_card_list = get_card_list(pages_list=startech_pages,card_tag='div.p-item-details')
startech_df = gpu_dataframe_card(card_list=startech_card_list,gpu_name_tag='h4.p-item-name > a',
                                gpu_price_tag='div.p-item-price > span',retailer_name='Startech Engineering')

logging.info(msg=f'Startech Engineering BD data scraped and stored to a dataframe successfully; length of dataframe = {len(startech_df)}')

# Techland BD
techlandbd_pages = get_pages(first_pg_link='https://www.techlandbd.com/pc-components/graphics-card?sort=p.price&order=ASC&fq=1',
                        url_tag_tag='a',
                        url_tag_str='>')['soup_list']
techlandbd_card_list = get_card_list(pages_list=techlandbd_pages,card_tag='div.product-thumb > div.caption')
techlandbd_df = gpu_dataframe_card(card_list=techlandbd_card_list,gpu_name_tag='div.name > a',
                                gpu_price_tag='div.price > div > span',retailer_name='Tech Land BD')

logging.info(msg=f'Tech Land BD data scraped and stored to a dataframe successfully; length of dataframe = {len(techlandbd_df)}')

# Skyland Computer BD
skyland_pages = get_pages_select(first_pg_link='https://www.skyland.com.bd/product-category/components/graphics-card/?instock_products=in&orderby=price',
                        url_tag='a.next.page-number')['soup_list']
skyland_card_list = get_card_list(pages_list=skyland_pages,card_tag='div.product-small.box div.box-text.box-text-products.text-center.grid-style-2')
skyland_df = woocommerce_gpu_dataframe_card(card_list=skyland_card_list,gpu_name_tag='div.title-wrapper > p > a',retailer_name='Skyland Computer Bd')

logging.info(msg=f'Skyland Computer BD data scraped and stored to a dataframe successfully; length of dataframe = {len(skyland_df)}')

# Ultra Technology BD
ultratech_pages = get_pages_select(first_pg_link='https://www.ultratech.com.bd/pc-components/graphics-card?sort=p.price&order=ASC&fq=1',
                        url_tag='a.next')['soup_list']
ultratech_card_list = get_card_list(pages_list=ultratech_pages,card_tag='div.product-thumb')
ultratech_df_0 = gpu_dataframe_card(card_list=ultratech_card_list,gpu_name_tag='div.name > a',gpu_price_tag='div.price > div > span',retailer_name='Ultra Technology')
# since some of the products that are currently not in stock are marked as BDT. 0 in the html code
ultratech_df = ultratech_df_0.loc[ultratech_df_0['gpu_price']!=0]

logging.info(msg=f'Ultra Technology data scraped and stored to a dataframe successfully; length of dataframe = {len(ultratech_df)}')

# Nexus Computer Bangladesh
nexusbd_pages = pagination_get_pages_select(first_pg_link='https://www.nexus.com.bd/graphics-card/?sort_by=price&sort_order=asc&layout=products_multicolumns&items_per_page=64&features_hash=13-Y',
                        url_tag='div#pagination_block_bottom > div.ty-pagination__items ~ a')['soup_list']
# cannot rely on 'manually' choosing non-empty cards; function to find non-empty cards programmatically
def get_nexusbd_non_empty_cards(pages_list,card_tag):
    """Gets a list devoid of all non-empty card divs from the list containing nexusbd pages
    Args:
        pages_list (list): List of nexusbd gpu pages as BeatifulSoup objects
        card_tag (bs4.element.ResultSet): Relative CSS path to get all the div cards containing gpu info
    Returns:
        list: list of all non-empty nexusbd card divs
    """
    card_list = []
    for page in pages_list:
        card_list.extend(page.select(card_tag))
    card_list_non_empty = list(filter(lambda card: card.get_text() != '', card_list))
    return card_list_non_empty
nexusbd_card_list = get_nexusbd_non_empty_cards(pages_list=nexusbd_pages,card_tag='div#categories_view_pagination_contents > div.ty-column4')
nexusbd_df = gpu_dataframe_card(card_list=nexusbd_card_list,gpu_name_tag='div.ut2-gl__name > a',
                                gpu_price_tag='span.ty-price > bdi > span ~ span',retailer_name='Nexus Technology')

logging.info(msg=f'Nexus Technology data scraped and stored to a dataframe successfully; length of dataframe = {len(nexusbd_df)}')

# Global Brand
# Global Brand only has a single page
globalbrand_pages = [bsoup(requests.get('https://www.globalbrand.com.bd/graphics-card?sort=p.price&order=ASC&limit=100').content,features='html.parser')]
globalbrand_card_list = globalbrand_pages[0].select('div.caption')
# # the following dataframe contains rows of '0 price', basically they are the unavailable ones. Thus, filterting them out into a new dataframe
globalbrand_df_0 = gpu_dataframe_card(card_list=globalbrand_card_list,gpu_name_tag='div.name > a',
                                gpu_price_tag='div.price > div > span',retailer_name='Global Brand')
globalbrand_df = globalbrand_df_0.loc[globalbrand_df_0['gpu_price']!=0]

logging.info(msg=f'Global Brand data scraped and stored to a dataframe successfully; length of dataframe = {len(globalbrand_df)}')

# Creatus Computer 
creatus_pages = get_pages_select(first_pg_link='https://creatuscomputer.com/category/components/graphics-card/?min_price=3000&max_price=352000&orderby=price',
                        url_tag='a.next.page-number')['soup_list']
creatus_card_list = get_card_list(pages_list=creatus_pages,card_tag='div.product-small.box div.box-text.box-text-products.text-center.grid-style-2')
creatus_df = woocommerce_gpu_dataframe_card_instock(card_list=creatus_card_list,gpu_name_tag='div.title-wrapper > p > a',retailer_name='Creatus Computer')

logging.info(msg=f'Cretaus Computer data scraped and stored to a dataframe successfully; length of dataframe = {len(creatus_df)}')

# UCC BD
uccbd_pages = [bsoup(requests.get('https://www.ucc.com.bd/category-store/computer-components/graphics-card?sort=p.price&order=ASC&fq=1&limit=100').content,features='html.parser')]
uccbd_card_list = get_card_list(pages_list=uccbd_pages,card_tag='div.product-thumb')
uccbd_df = gpu_dataframe_card(card_list=uccbd_card_list,gpu_name_tag='div.caption > div.name > a',gpu_price_tag='div.price > div > span',retailer_name='UCC-BD')

logging.info(msg=f'UCC-BD data scraped and stored to a dataframe successfully; length of dataframe = {len(uccbd_df)}')

list_of_df = [ryans_df,startech_df,techlandbd_df,skyland_df,ultratech_df,nexusbd_df,globalbrand_df,creatus_df,uccbd_df]
master_df = pd.concat(list_of_df)

logging.info(msg=f'All dataframes compiled into master_df of length {len(master_df)}')
logging.info(msg=f'Number of retailers in master df is {len(master_df.retailer_name.unique())}, while length of list_of_df is {len(list_of_df)}')

# any row which has a GPU price of 0 should be discarded
master_df = master_df.loc[master_df.gpu_price!=0]

# rounding the GPU Prices to their nearest hundreds
import math
master_df['gpu_price']=master_df['gpu_price'].apply(lambda x: 100 * math.ceil(x/100))

# list of all gpu units of interest
with open('./gpu_units_of_interest/geforce_gpu_units.txt','r') as reader_geforce:
    geforce_gpu_unit_read = reader_geforce.read()
    geforce_gpu_unit_list = geforce_gpu_unit_read.split('\n')
geforce_gpu_unit_list
reader_geforce.close()

logging.info(msg='Added list of Geforce GPUs from file')

with open('./gpu_units_of_interest/radeon_gpu_units.txt','r') as reader_radeon:
    radeon_gpu_unit_read = reader_radeon.read()
    radeon_gpu_unit_list = radeon_gpu_unit_read.split('\n')
radeon_gpu_unit_list
reader_radeon.close()

logging.info(msg='Added list of Radeon GPUs from file')

with open('./gpu_units_of_interest/intel_gpu_units.txt','r') as reader_intel:
    intel_gpu_unit_read = reader_intel.read()
    intel_gpu_unit_list = intel_gpu_unit_read.split('\n')
intel_gpu_unit_list
reader_intel.close()

logging.info(msg='Added list of Intel GPUs from file')

logging.info(msg=f'Total number of GPUs = {len(geforce_gpu_unit_list+radeon_gpu_unit_list+intel_gpu_unit_list)}')

# creating dataframes with GPU unit names in each row
def add_gpu_unit_name(target_df,gpu_list,gpu_brand):
    """creates a dataframe from a larger dataframe (intended to be created from master_df), and add GPU unit names to each row
    Args:
        target_df (pandas DataFrame): the dataframe (mainly master_df) from which smaller dataframes will be extracted
        gpu_list (list): list of GPU unit names, smaller dataframe from target_df will be extracted corresponding to each list entry
        gpu_brand (string): the brand name of the GPU (Geforce/Intel Arc/Radeon)
    Returns:
        pandas DataFrame: dataframe containing the graphics cards corresponding to each GPU in gpu_of_interest
    """
    gpu_base_name_df = pd.DataFrame()
    for gpu in gpu_list:
        df_with_gpu_name = target_df.loc[target_df['gpu_name'].str.contains(re.compile(gpu,flags=re.I))]
        # in some websites, there are no spaces within the gpu names (e.g. RTX3080)
        # thus bringing all the rest of the names into a common format with no space within gpu names
        gpu_nospace = gpu.replace(' ','')
        df_with_gpu_name_nospace = target_df.loc[target_df['gpu_name'].str.contains(re.compile(gpu_nospace,flags=re.I))]
        df_with_gpu_name['gpu_unit_name'] = gpu_brand + ' ' +gpu
        gpu_base_name_df = pd.concat([gpu_base_name_df,df_with_gpu_name,df_with_gpu_name_nospace])
        gpu_base_name_df.drop_duplicates(subset='retail_url',keep='last',inplace=True)
    return gpu_base_name_df

# all geforce gpu's
geforce_gpu_df = add_gpu_unit_name(master_df,geforce_gpu_unit_list,'Geforce')
geforce_gpu_df.reset_index(drop=True,inplace=True)
# GTX 1050 Ti are written in varying formats across websites (e.g. GTX 1050ti, GTX 1050 Ti, GTX1050Ti)
# and there are no GTX 1050's available, so it is just easier to make a separate dataframe for it
df_1050_ti = master_df.loc[master_df['gpu_name'].str.contains('1050')]
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

geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce GTX 1650','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(gddr5_vs_gddr6_1650)

# significant performance difference between RTX 3080 10GB and 12GB variants
def rtx_3080_10_vs_12(gpu_3080):
    """the rtx 3080 10 and 12GB versions have significant performace difference,
       this function distinguishes between them (to be applied with the .apply() method in dataframe)
    Args:
        gpu_3080 (string): RTX 3080 GPU name (as listed on retailer website)
    Returns:
        string: "RTX 3080 10GB"/"RTX 3080 12GB"
    """
    # sometimes the retailer names have the full '12 GB'/'10 GB' spelled out, sometimes it just has '12G'/'10G' in the name
    regex_match = re.search(pattern='12gb|12g',string=gpu_3080,flags=re.I)
    if bool(regex_match)==True:
        return 'Geforce RTX 3080 12GB'
    else:
        return 'Geforce RTX 3080 10GB'

geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce RTX 3080','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(rtx_3080_10_vs_12)

# Nvidia 'stealth-launched the RTX 3080 8GB variant, and has a much lower performance compared to the 
# original RTX 3080 (which had 12GB)
def rtx_3060_8_vs_12(gpu_3060):
    """function to distinguish between the rtx 3060 12GB and the rtx 3060 8GB; thanks for scamming the customers
       and making my life harder, Nvidia. In the words of Linus Torvald:
       Nvidia! F*** you!
    Args:
        gpu_3060 (string): RTX 3060 GPU name (as listed on retailer website)
    Returns:
        string: "RTX 3060 12GB"/"RTX 3060 8GB"
    """
    regex_match = re.search(pattern='8gb|8g',string=gpu_3060,flags=re.I)
    if bool(regex_match)==True:
        return 'Geforce RTX 3060 8GB'
    else:
        return 'Geforce RTX 3060 12GB'

geforce_gpu_df.loc[geforce_gpu_df['gpu_unit_name']=='Geforce RTX 3060','gpu_unit_name'] = geforce_gpu_df['gpu_name'].apply(rtx_3060_8_vs_12)

# all radeon and intel gpu's
radeon_gpu_df = add_gpu_unit_name(master_df,radeon_gpu_unit_list,'Radeon')
intel_arc_gpu_df = add_gpu_unit_name(master_df,intel_gpu_unit_list,'Intel')

# all graphics cards of interest
gpu_of_interest_df = pd.concat([geforce_gpu_df,radeon_gpu_df,intel_arc_gpu_df,df_1050_ti])
gpu_of_interest_df.reset_index(drop=True,inplace=True)

logging.info(f'gpu_of_interest_df created with {len(gpu_of_interest_df)} entries')

# temporarily adding to excel files for gpu_of_interest_df
with pd.ExcelWriter('./output_files/gpu_of_interest.xlsx', mode="a", engine="openpyxl",if_sheet_exists='replace') as writer:
    gpu_of_interest_df.to_excel(writer,sheet_name='Sheet1',header=True)
    writer.close

logging.info(f'Written gpu_of_interest_df to excel file')

# lowest prices of each gpu unit
lowest_price_df=gpu_of_interest_df[gpu_of_interest_df['gpu_price'] == gpu_of_interest_df.groupby('gpu_unit_name')['gpu_price'].transform(min)]
lowest_price_df.reset_index(drop=True,inplace=True)

logging.info(f'lowest_price_df created with {len(lowest_price_df)} entries')

# temporarily adding to excel files for lowest_price_df
with pd.ExcelWriter('./output_files/gpu_of_interest.xlsx', mode="a", engine="openpyxl",if_sheet_exists='overlay') as writer_lowest:
    lowest_price_df.to_excel(writer_lowest,sheet_name='lowest_price',startrow=writer_lowest.sheets['lowest_price'].max_row,header=not os.path.exists('./output_files/gpu_of_interest.xlsx'))
    writer_lowest.close

logging.info('Written lowest_price_df to excel file')

# creating a tiered lowest_prices table

from overall_tier_score import overall_tier_score_df

lowest_prices_tiered=pd.merge(
    left=lowest_price_df,
    right=overall_tier_score_df[['gpu_unit_name','base_tier_score', 'net_tier_score', 'non_rt_net_score']],
    on='gpu_unit_name'
    )

logging.info(f'lowest_prices_tiered dataframe created with {len(lowest_prices_tiered)} rows and {len(lowest_prices_tiered.columns)} column')

# adding price per tier score columns to dataframe

lowest_prices_tiered['price_per_base_tier'] = lowest_prices_tiered['gpu_price']/lowest_prices_tiered['base_tier_score']
lowest_prices_tiered['price_per_net_tier'] = lowest_prices_tiered.gpu_price/lowest_prices_tiered.net_tier_score
lowest_prices_tiered['price_per_non_rt_tier'] = lowest_prices_tiered.gpu_price/lowest_prices_tiered.non_rt_net_score

logging.info(
    f'3 columns added to lowest_prices_tiered dataframe being {lowest_prices_tiered.columns[-3]}, {lowest_prices_tiered.columns[-2]} and {lowest_prices_tiered.columns[-1]}')

with pd.ExcelWriter('./output_files/gpu_of_interest.xlsx',mode='a',engine='openpyxl',if_sheet_exists='replace') as lowest_price_tier_writer:
    lowest_prices_tiered.to_excel(
        lowest_price_tier_writer,
        sheet_name='lowest_prices_tiered'
    )
    lowest_price_tier_writer.close

logging.info(f'lowest_prices_tiered dataframe written to Excel file with {len(lowest_prices_tiered)} rows')


# loading the previous dataframes into databases

load_dotenv()

db_host = os.getenv("pgsql_host")
db_user = os.getenv("pgsql_user")
db_port = os.getenv("pgsql_port")
db_passwd = os.getenv("pgsql_password")
db_database = os.getenv("pgsql_db")

pgsql_db_engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_database}')

logging.info(msg='Connection to database established')

gpu_of_interest_df.to_sql(name='gpu_of_interest',con=pgsql_db_engine,if_exists='replace',index=False)
lowest_price_df.to_sql(name='lowest_prices',con=pgsql_db_engine,if_exists='append',index=False)
lowest_prices_tiered.to_sql(name='lowest_prices_tiered',con=pgsql_db_engine,if_exists='replace',index=False)

logging.info(msg='All dataframes written to database\n')