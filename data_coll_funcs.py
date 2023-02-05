import requests
from bs4 import BeautifulSoup as bsoup
import pandas as pd
import re
import time
import os


# function to get all the gpu pages of a website
# returns both a list of gpu pages url and the gpu pages as BeautifulSoup objects
def get_pages(first_pg_link,url_tag_tag,url_tag_str):
    """gets all the pages with the list of gpu's for that website from the first page link, and the html element 
       for going to the next page

    Args:
        first_pg_link (string): the link of the first page for the list of gpu's in that website 
                                (i.e. page 1 of x, for x pages containing the entire list of gpu's)
        url_tag_tag (string): the html tag which contains the link to the next page
        url_tag_str (string): the string used on the page to indicate next page (e.g. '>' or 'NEXT')

    Returns:
        dict: a dictionary containing the list of url's of each page as key, and the list of pages (as BeautifulSoup objects) as values
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []

    while(True):
        page_content = requests.get(next_pg_link).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.find_all(url_tag_tag,string=url_tag_str)
        if link_tag == []:
            break
        next_pg_link = link_tag[0]['href']
        url_list.append(next_pg_link)
        # execution delay (so I don't accidentally ddos them :|)
        time.sleep(1)
        url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}
        
    return url_and_pages_dict


def get_pages_select(first_pg_link,url_tag):
    """ similar to get_pages, gets all the pages with the list of gpu's for that website from the first page link, and the html element 
       for going to the next page, but with BeautifulSoup's select() method

    Args:
        first_pg_link (string): the link of the first page for the list of gpu's in that website 
        url_tag (string): the interactible html tag to go the next page

    Returns:
        dict: a dictionary containing the list of url's of each page as key, and the list of pages (as BeautifulSoup objects) as values
    """
    next_pg_link = first_pg_link
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []
    while(True):
        page_content = requests.get(next_pg_link).content
        page_soup = bsoup(page_content,features='html.parser')
        pages_list.append(page_soup)
        link_tag = page_soup.select(url_tag)
        if link_tag == []:
            break
        next_pg_link = link_tag[0]['href']
        url_list.append(next_pg_link)
        # execution delay (so I don't accidentally ddos them :|)
        time.sleep(1)
        url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}

    return url_and_pages_dict
# --new function--
# function to get the list of all tags containing the gpu names
def gpu_names_tags_select(pages_list,gpu_names_tag):
    # making a list containing all the gpu names obtained from the above line
    name_tag_list = []
    for page in pages_list:
        # finding all tags with the attributes containing gpu names
        name_tag_list.extend(page.select(gpu_names_tag))
    return name_tag_list
# --new function--
# function to get the list of gpu names from the list of gpu name tags
def gpu_names(name_tag_list):
    # empty list for storing gpu names
    gpu_names_list = []
    # loop through every entry in the name_tag_list and append to a gpu_names_list
    for gpu_name in name_tag_list:
        gpu_names_list.append(gpu_name.get_text())
    return gpu_names_list
# --new function--
# function to get the list of all tags containing prices
def gpu_price_tags_select(pages_list,price_tag):
    # making an empty list to append price tag list of every pages to
    price_tags_list = []
    # looping through every page in the pages list
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
    # dataframe containing two columns - 'gpu_name' and 'Price'
    gpu_df = pd.DataFrame(data={'gpu_name':gpu_names_list,'Price':gpu_price_list})
    return gpu_df
# --new function--
# function to get a list of cards containing the gpu names and price information from all pages
def get_card_list(pages_list,card_tag):
    # empty list to contain all the cards containing the divs containing the names and prices
    card_list = []
    # getting a list of all divs that contain both the name and card info for each of the pages
    for page in pages_list:
        card_list.extend(page.select(card_tag))
    return card_list
# --new function--
# function to get a dataframe containing the gpu name, price, retailer url, date of data collection and retailer name
def gpu_dataframe_card(card_list,gpu_name_tag,gpu_price_tag,retailer_name):
    # defining a dict for storing the names and prices. names will be keys and prices will be values
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url']) 
    # loop through each card in ryans_card_list to get the names and prices
    for card in card_list:
        # get the name of the gpu from the card
        gpu_name = card.select(gpu_name_tag)[0].get_text()
        # getting the url of the gpu
        gpu_url = card.select(gpu_name_tag)[0]['href']
        price_tag = card.select(gpu_price_tag)
        if price_tag == []:
            continue
        price_text = price_tag[0].get_text()
        # getting only the digits from the price_text and turning it into integer type
        price = int(re.findall('\d+', price_text.replace(',',''))[0])
        gpu_df_card.loc[len(gpu_df_card.index)] = [gpu_name, price, gpu_url] 
    # adding a column for data collection date
    gpu_df_card['data_collection_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    # adding a column for the retailer name
    gpu_df_card['retailer_name'] = retailer_name
    return gpu_df_card
# --new function--
# function to save dataframe into csv file; create new file if file didn't exist, or append to it if it did exist
def df_to_csv(gpu_df,save_path,retailer_prefix):
    return gpu_df.to_csv(path_or_buf=save_path+retailer_prefix+'_csv.csv',mode='a', header=not os.path.exists(save_path+retailer_prefix+'_csv.csv'))
# --new function--
# for sites that used woocommerce
def woocommerce_gpu_dataframe_card(card_list,gpu_name_tag,retailer_name):
    # defining a dict for storing the names and prices. names will be keys and prices will be values
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url']) 
    # loop through each card in ryans_card_list to get the names and prices
    for card in card_list:
        # get the name of the gpu from the card
        gpu_name = card.select(gpu_name_tag)[0].get_text()
        # getting the url of the gpu
        gpu_url = card.select(gpu_name_tag)[0]['href']
        # the parent tag for price is ultimately 'div.price-wrapper'. For gpu's with no discount,
        # the price is in a bdi tag inside of a span, inside another span, which in turn is contained in div.price-wrapper
        price_tag = card.select('div.price-wrapper > span > span > bdi')
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
    # adding a column for data collection date
    gpu_df_card['data_collection_date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    # adding a column for the retailer name
    gpu_df_card['retailer_name'] = retailer_name
    return gpu_df_card
# --new function--
# selecting only 'In Stock' cards for woocommerce sites
def woocommerce_gpu_dataframe_card_instock(card_list,gpu_name_tag,retailer_name):
    # defining a dict for storing the names and prices. names will be keys and prices will be values
    gpu_df_card = pd.DataFrame(columns=['gpu_name','gpu_price','retail_url']) 
    # loop through each card in ryans_card_list to get the names and prices
    for card in card_list:
        stock_status_str=card.select('p.stock')[0].get_text()
        if re.findall(pattern='In Stock',string=stock_status_str,flags=re.I):
            # get the name of the gpu from the card
            gpu_name = card.select(gpu_name_tag)[0].get_text()
            # getting the url of the gpu
            gpu_url = card.select(gpu_name_tag)[0]['href']
            # the parent tag for price is ultimately 'div.price-wrapper'. For gpu's with no discount,
            # the price is in a bdi tag inside of a span, inside another span, which in turn is contained in div.price-wrapper
            price_tag = card.select('div.price-wrapper > span > span > bdi')
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

# Nexus Technology BD has 'pagination' in most html tags
def pagination_get_pages_select(first_pg_link,url_tag):
    next_pg_link = first_pg_link
    # list of each gpu pages url
    url_list = [first_pg_link]
    # list of pages as BeautifulSoup objects
    pages_list = []
    while(True):
        # getting the page content
        page_content = requests.get(next_pg_link).content
        # turn the page content into BeautifulSoup object
        page_soup = bsoup(page_content,features='html.parser')
        # add the page
        pages_list.append(page_soup)
        # get the link to the next page
        # finding the tag with a particular string, that will contain our next page link
        link_tag = page_soup.select(url_tag)
        # if link_tag produces an empty list, the loop breaks
        if link_tag == []:
            break
        # since nexus' last page has an 'a' tag with no 'href', I have to use try-except here
        try:
            # storing the next page link
            next_pg_link = link_tag[0]['href']
        except(KeyError):
            break
        # adding the link to the url_list
        url_list.append(next_pg_link)
        # execution delay (so I don't accidentally ddos them :|)
        time.sleep(1)
        # a dictionary containing both the list of urls and the list of soups, to be the return value of the method
        url_and_pages_dict = {'url_list':url_list,'soup_list':pages_list}
    return url_and_pages_dict