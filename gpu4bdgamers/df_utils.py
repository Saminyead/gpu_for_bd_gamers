import pandas as pd
import re

def add_gpu_unit_name(target_df,gpu_list,gpu_brand):
    """creates a dataframe from a larger dataframe (intended to be created from master_df), and add GPU unit names to each row
    Args:
        target_df (pandas DataFrame): the dataframe (mainly master_df) from which smaller dataframes will be extracted
        gpu_list (list): list of GPU unit names, smaller dataframe from target_df will be extracted corresponding to each list entry
        gpu_brand (string): the brand name of the GPU (Geforce/Intel Arc/Radeon)
    Returns:
        pandas.DataFrame: dataframe containing the graphics cards corresponding to each GPU in gpu_of_interest
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
