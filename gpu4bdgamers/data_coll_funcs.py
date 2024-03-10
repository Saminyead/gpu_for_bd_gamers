import requests
from bs4 import BeautifulSoup as bsoup
import pandas as pd
import re
import time
import os



def get_pages_find_all(first_pg_link:str,url_tag_str:str) -> dict:
    """gets all the pages with the list of gpu's for that website from the first page link, and the html element 
       for going to the next page

    Args:
        first_pg_link (str): the link of the first page for the list of gpu's in that website 
                                (i.e. page 1 of x, for x pages containing the entire list of gpu's)
        url_tag_tag (str): the html tag which contains the link to the next page
        url_tag_str (str): the string used on the page to indicate next page (e.g. '>' or 'NEXT')

    Returns:
        dict: a dictionary containing the list of url's of each page as key, and the list of pages (as BeautifulSoup objects) as values
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_soup_list = []

    while(True):
        page_content = requests.get(next_pg_link).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_soup_list.append(page_soup)
        link_tag = page_soup.find_all(name="a",string=url_tag_str)

        if not link_tag:
            break

        try:
            next_pg_link = link_tag[0]['href']
            url_list.append(next_pg_link)
            # execution delay (so I don't accidentally ddos them :|)
            time.sleep(1)

        except IndexError:
            break

    url_and_pages_dict = {'url_list':url_list,'soup_list':pages_soup_list}
        
    return url_and_pages_dict



def get_pages_select(first_pg_link,css_selector):
    """ similar to get_pages, gets all the pages with the list of gpu's for that website from the first page link, and the html element 
       for going to the next page, but with BeautifulSoup's select() method

    Args:
        first_pg_link (string): the link of the first page for the list of gpu's in that website 
        css_selector (string): the css selector to go to the next page

    Returns:
        dict: a dictionary containing the list of url's of each page as key, and the list of pages 
        (as BeautifulSoup objects) as values
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []
    while(True):
        page_content = requests.get(next_pg_link).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.select(css_selector)

        if not link_tag:
            break
        
        try:
            next_pg_link = link_tag[0]['href']
            url_list.append(next_pg_link)
            # execution delay (so I don't accidentally ddos them :|)
            time.sleep(1)

        except IndexError:
            break

    url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}

    return url_and_pages_dict



# Nexus Technology BD has 'pagination' in most html tags
def get_pages_select_pagination(first_pg_link:str,css_selector:str):
    """get_pages function for Nexus Technology BD website

    Args:
        first_pg_link (str): The first page link when searching for GPU's and ordering them 
        according to price
        css_selector (str): The CSS selector tag containing the next page link

    Returns:
        dict: a dictionary containing the list of url's of each page as key, and the list of pages 
        (as BeautifulSoup objects) as values
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    
    pages_list = []
    
    while(True):
        page_content = requests.get(next_pg_link).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.select(css_selector)
        
        if not link_tag:
            break

        # since nexus' last page has an 'a' tag with no 'href', I have to use try-except here
        try:
            next_pg_link = link_tag[0]['href']
        
        except(KeyError):
            break

        url_list.append(next_pg_link)
        time.sleep(1)
        url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}

    return url_and_pages_dict



def get_pages_single_page(first_pg_link:str) -> dict:
    pages_soup = [bsoup(requests.get(first_pg_link).content,features='html.parser')]
    url_and_pages_dict = {'url_list':[first_pg_link],'soup_list':pages_soup}

    return url_and_pages_dict



# function to get a list of cards containing the gpu names and price information from all pages
def get_card_list(pages_list:list,card_css_selector:str):
    """gets the list of all cards containing the GPU name and pricing information

    Args:
        pages_list (list): list of pages as beautifulsoup objects
        card_css_selector (str): the css selector of the card

    Returns:
        list: list of cards of all pages of a particular website
    """
    card_list = []
    for page in pages_list:
        card_list.extend(page.select(card_css_selector))
    
    # nexusbd has a bunch of empty card divs, thus separate 'get_card_list' function
    card_list_non_empty = list(filter(lambda card: card.get_text() != '', card_list))

    return card_list_non_empty


# function to get the list of all tags containing the gpu names
def gpu_names_tags_select(pages_list,gpu_names_tag):
    """gets a list of all tags containing the GPU names in a page

    Args:
        pages_list (list): list of pages (generally, the output of get_pages() or get_pages_select()), each page being a BeautifulSoup object
        gpu_names_tag (string): tag denoting the GPU names

    Returns:
        list: list of tags containing the GPU names in their texts
    """
    name_tag_list = []
    for page in pages_list:
        name_tag_list.extend(page.select(gpu_names_tag))
    return name_tag_list



def gpu_names(name_tag_list):
    """gets the list of GPU names from a list of GPU names tags

    Args:
        name_tag_list (list): list of tags where the inner texts are the GPU names

    Returns:
        list: list of GPU names
    """
    gpu_names_list = []
    for gpu_name in name_tag_list:
        gpu_names_list.append(gpu_name.get_text())
    return gpu_names_list


# function to get the list of all tags containing prices
def gpu_price_tags_select(pages_list,price_tag):
    # making an empty list to append price tag list of every pages to
    price_tags_list = []
    
    for page in pages_list:
        price_tags_list.extend(page.select(price_tag))
    return price_tags_list



# --new function--
# function to get the list of all gpu prices from the price_tags_list
def gpu_prices(price_tags_list):
    # loop through every element in the list to get the inner element
    gpu_price_list = [price_tag.get_text() for price_tag in price_tags_list]
    return gpu_price_list


# --new function--
# function to add the gpu_names_list and gpu_price_list to a dataframe
def gpu_dataframe(gpu_names_list,gpu_price_list):
    gpu_df = pd.DataFrame(data={'gpu_name':gpu_names_list,'Price':gpu_price_list})
    return gpu_df



def gpu_dataframe_card(
    card_list:list,
    gpu_name_css_sel:str,
    gpu_price_css_sel:str,
    retailer_name:str) -> pd.DataFrame:
    """get a dataframe containing the gpu name, price, retailer url, date of data collection and retailer name

    Args:
        card_list (list): list of divs (cards) in the website containing the gpu information including name and price
        gpu_name_css_sel (str): the css selector using which the gpu name can be obtained
        gpu_price_css_sel (str): css selector using which the price can be obtained
        retailer_name (str): name of the retailer

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url'])
    
    for card in card_list:
        gpu_name = card.select(gpu_name_css_sel)[0].get_text()
        gpu_url = card.select(gpu_name_css_sel)[0]['href']
        price_tag = card.select(gpu_price_css_sel)
        if not price_tag:
            continue
        
        price_text = price_tag[0].get_text()
        price = int(re.findall('\d+', price_text.replace(',',''))[0])
        
        gpu_df_card.loc[len(gpu_df_card.index)] = [gpu_name, price, gpu_url] 
    
    gpu_df_card['data_collection_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    gpu_df_card['retailer_name'] = retailer_name
    
    return gpu_df_card



def retry_with_scraperapi_pages_find_all(
    scraperapi_api_key:str,
    first_pg_link:str,
    url_tag_str:str,
    card_css_selector:str,
    gpu_name_css_sel:str,
    gpu_price_css_sel:str,
    retailer_name:str) -> pd.DataFrame:

    """If the dataframe from a retail website has 0 len, then retry scraping with scraperapi (for websites scraped with get_pages_find_all)

    Args:
        first_pg_link (str): when gpu is arranged by price in a website, the link of the first page containing the list of gpus
        url_tag_str (str): the string of the a tag, where if clicked, would go to the next page
        card_css_selector (str): the css selector to get cards containing the gpu
        gpu_name_css_sel (str): the css selector to get the name of the gpu
        gpu_price_css_sel (str): the css selector to get the price of the gpu
        retailer_name (str): the name of the retailer whose website it is

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_soup_list = []

    while(True):
        payload = {'api_key': scraperapi_api_key, 'url': next_pg_link, 'render':'true'}
        page_content = requests.get('http://api.scraperapi.com', params=payload).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_soup_list.append(page_soup)
        link_tag = page_soup.find_all(name="a",string=url_tag_str)

        if not link_tag:
            break

        try:
            next_pg_link = link_tag[0]['href']
            url_list.append(next_pg_link)
            # execution delay (so I don't accidentally ddos them :|)
            time.sleep(1)

        except IndexError:
            break

    url_and_pages_dict = {'url_list':url_list,'soup_list':pages_soup_list}

    card_list = get_card_list(
        pages_list=url_and_pages_dict['pages_soup_list'],
        card_css_selector=card_css_selector
    )
    
    df = gpu_dataframe_card(
        card_list=card_list,
        gpu_name_css_sel=gpu_name_css_sel,
        gpu_price_css_sel=gpu_price_css_sel,
        retailer_name=retailer_name
    )

    return df


def retry_with_scraperapi_pages_select(
    scraperapi_api_key:str,
    first_pg_link:str,
    pages_css_selector:str,
    card_css_selector:str,
    gpu_name_css_sel:str,
    gpu_price_css_sel:str,
    retailer_name:str) -> pd.DataFrame:

    """If the dataframe from a retail website has 0 len, then retry scraping with scraperapi (for websites scraped with get_pages_select)

    Args:
        first_pg_link (str): when gpu is arranged by price in a website, the link of the first page containing the list of gpus
        pages_css_selector (str): the css selector to go to the next page
        card_css_selector (str): the css selector to get cards containing the gpu
        gpu_name_css_sel (str): the css selector to get the name of the gpu
        gpu_price_css_sel (str): the css selector to get the price of the gpu
        retailer_name (str): the name of the retailer whose website it is

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []
    while(True):
        payload = {'api_key': scraperapi_api_key, 'url': next_pg_link, 'render':'true'}
        page_content = requests.get('http://api.scraperapi.com', params=payload).content
        
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.select(pages_css_selector)

        if not link_tag:
            break
        
        try:
            next_pg_link = link_tag[0]['href']
            url_list.append(next_pg_link)
            # execution delay (so I don't accidentally ddos them :|)
            time.sleep(1)

        except IndexError:
            break

    url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}
    
    card_list = get_card_list(
        pages_list=url_and_pages_dict['pages_list'],
        card_css_selector=card_css_selector
    )

    df = gpu_dataframe_card(
        card_list=card_list,
        gpu_name_css_sel=gpu_name_css_sel,
        gpu_price_css_sel=gpu_price_css_sel,
        retailer_name=retailer_name
    )
    
    return df


def retry_with_scraperapi_creatus(
    scraperapi_api_key:str,
    first_pg_link:str,
    pages_css_selector:str,
    card_css_selector:str,
    gpu_name_css_sel:str,
    retailer_name:str="Creatus Computer") -> pd.DataFrame:

    """If the dataframe from a retail website has 0 len, then retry scraping with scraperapi (made specifically for creatus computer)

    Args:
        first_pg_link (str): when gpu is arranged by price in a website, the link of the first page containing the list of gpus
        pages_css_selector (str): the css selector to go to the next page
        card_css_selector (str): the css selector to get cards containing the gpu
        gpu_name_css_sel (str): the css selector to get the name of the gpu
        gpu_price_css_sel (str): the css selector to get the price of the gpu
        retailer_name (str): the name of the retailer whose website it is

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []
    while(True):
        payload = {'api_key': scraperapi_api_key, 'url': next_pg_link, 'render':'true'}
        page_content = requests.get('http://api.scraperapi.com', params=payload).content
        
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.select(pages_css_selector)

        if not link_tag:
            break
        
        try:
            next_pg_link = link_tag[0]['href']
            url_list.append(next_pg_link)
            # execution delay (so I don't accidentally ddos them :|)
            time.sleep(1)

        except IndexError:
            break

    url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}
    
    card_list = get_card_list(
        pages_list=url_and_pages_dict['soup_list'],
        card_css_selector=card_css_selector
    )

    df = woocommerce_gpu_dataframe_card_instock(
        card_list=card_list,
        gpu_name_tag=gpu_name_css_sel,
        retailer_name=retailer_name
    )
    
    return df


def retry_with_scraperapi_pages_select_pagination(
    first_pg_link:str,
    pages_css_selector:str,
    card_css_selector:str,
    gpu_name_css_sel:str,
    gpu_price_css_sel:str,
    retailer_name:str) -> pd.DataFrame:
    """If the dataframe from a retail website has 0 len, then retry scraping with scraperapi (for websites scraped with get_pages_select_pagination)

    Args:
        first_pg_link (str): when gpu is arranged by price in a website, the link of the first page containing the list of gpus
        pages_css_selector (string): the css selector to go to the next page
        card_css_selector (str): the css selector to get cards containing the gpu
        gpu_name_css_sel (str): the css selector to get the name of the gpu
        gpu_price_css_sel (str): the css selector to get the price of the gpu
        retailer_name (str): the name of the retailer whose website it is

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    pages = get_pages_select_pagination(first_pg_link=first_pg_link,css_selector=pages_css_selector)
    card_list = get_card_list(pages_list=pages,card_css_selector=card_css_selector)
    df = gpu_dataframe_card(
        card_list=card_list,
        gpu_name_css_sel=gpu_name_css_sel,
        gpu_price_css_sel=gpu_price_css_sel,
        retailer_name=retailer_name
    )
    
    return df



def retry_with_scraperapi_pages_select_single_page(
    first_pg_link:str,
    card_css_selector:str,
    gpu_name_css_sel:str,
    gpu_price_css_sel:str,
    retailer_name:str) -> pd.DataFrame:
    """If the dataframe from a retail website has 0 len, then retry scraping with scraperapi (for websites scraped with get_pages_single_page)

    Args:
        first_pg_link (str): when gpu is arranged by price in a website, the link of the first page containing the list of gpus
        card_css_selector (str): the css selector to get cards containing the gpu
        gpu_name_css_sel (str): the css selector to get the name of the gpu
        gpu_price_css_sel (str): the css selector to get the price of the gpu
        retailer_name (str): the name of the retailer whose website it is

    Returns:
        pd.DataFrame: dataframe containing gpu name, price, retailer url, data collection date and retailer name
    """
    pages = get_pages_single_page(first_pg_link=first_pg_link)
    card_list = get_card_list(pages_list=pages,card_css_selector=card_css_selector)
    df = gpu_dataframe_card(
        card_list=card_list,
        gpu_name_css_sel=gpu_name_css_sel,
        gpu_price_css_sel=gpu_price_css_sel,
        retailer_name=retailer_name
    )
    
    return df



# --new function--
def df_to_csv(gpu_df:pd.DataFrame,save_path:str,retailer_prefix:str):
    gpu_df.to_csv(path_or_buf=save_path+retailer_prefix+'_csv.csv',mode='a', header=not os.path.exists(save_path+retailer_prefix+'_csv.csv'))




# --new function--
# for sites that used woocommerce
def woocommerce_gpu_dataframe_card(card_list,gpu_name_tag,retailer_name):
    # defining a dict for storing the names and prices. names will be keys and prices will be values
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url']) 

    for card in card_list:
        gpu_name = card.select(gpu_name_tag)[0].get_text()
        gpu_url = card.select(gpu_name_tag)[0]['href']
        price_tag = card.select('div.price-wrapper > span > span > bdi')
        if price_tag == []:
            # for discounted price
            price_tag = card.select('div.price-wrapper > span > ins > span > bdi')
        
        # for cards with no price information
        try:
            price_text = price_tag[0].get_text()
        except(IndexError):
            continue
        
        price = int(re.findall('\d+', price_text.replace(',',''))[0])
        gpu_df_card.loc[len(gpu_df_card.index)] = [gpu_name, price, gpu_url] 
    
    gpu_df_card['data_collection_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    gpu_df_card['retailer_name'] = retailer_name
    return gpu_df_card



# --new function--
# selecting only 'In Stock' cards for woocommerce sites
def woocommerce_gpu_dataframe_card_instock(card_list,gpu_name_tag,retailer_name):
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url']) 
    for card in card_list:
        stock_status_str=card.select('p.stock')[0].get_text()
        if re.findall(pattern='In Stock',string=stock_status_str,flags=re.I):
            # get the name of the gpu from the card
            gpu_name = card.select(gpu_name_tag)[0].get_text()
            # getting the url of the gpu
            gpu_url = card.select(gpu_name_tag)[0]['href']
            # the parent tag for price is ultimately 'div.price-wrapper'. For gpu's with no discount,
            # the price is in a bdi tag inside of a span, inside another span, which in turn is contained in div.price-wrapper
            price_tag = card.select('div.price > span.price-new')
            if price_tag == []:
                # this case is for discounted price, when the bdi tag is inside a span, which is actually inside an ins tag
                price_tag = card.select('div.price-wrapper > span > ins > span > bdi')
            # this is for when there is no price information on the cards. There are quite a few on the Skyland Computer BD website
            try:
                price_text = price_tag[0].get_text()
            except(IndexError):
                continue
            # getting only the digits from the price_text and turning it into integer type
            price = int(re.findall('\d+', price_text.replace(',',''))[0])
            gpu_df_card.loc[len(gpu_df_card.index)] = [gpu_name, price, gpu_url] 
        else:
            continue
    # adding a column for data collection date
    gpu_df_card['data_collection_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    # adding a column for the retailer name
    gpu_df_card['retailer_name'] = retailer_name
    return gpu_df_card



def gpu_version_diff(string:str,gpu_name:str,pattern_version_dict:dict):
    """for differentiating between 2 different versions of GPU in the gpu dataframes (for example, RX 
        580 4GB vs 8GB) using regex

    Args:
        string (str): the full name of the gpu as listed in the retailer website
        gpu_name (str): the base name of the gpu
        pattern_version_dict (dict): a dictionary containing the pattern (using which the GPU version 
            is to be differentiated) as the key and the suffix (e.g. 8GB) to be added to the GPU name

    Returns:
        str: the gpu name and version
    """
    for key,value in pattern_version_dict.items():
        regex_match = re.search(pattern=key,string=string,flags=re.I)
        if bool(regex_match)==True:
            gpu_version = f"{gpu_name} {value}"
            return gpu_version