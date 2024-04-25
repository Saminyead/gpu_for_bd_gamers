import pandas as pd
import re

def add_gpu_unit_name(
        target_df:pd.DataFrame,
        gpu_list:list[str],
        gpu_brand:str
) -> pd.DataFrame:
    """creates a dataframe from a larger dataframe (intended to be created 
    from master_df), and add GPU unit names to each row
    
    Args:
        target_df (pandas DataFrame): the dataframe (mainly master_df) 
            from which smaller dataframes will be extracted
        gpu_list (list): list of GPU unit names, smaller dataframe from 
            target_df will be extracted corresponding to each list entry
        gpu_brand (string): the brand name of the GPU (Geforce/Intel Arc/Radeon)
    Returns:
        pandas.DataFrame: dataframe containing the graphics cards corresponding 
            to each GPU in gpu_of_interest
    """
    gpu_base_name_df = pd.DataFrame()

    for gpu in gpu_list:
        df_with_gpu_name = target_df.loc[
            target_df['gpu_name'].str.contains(re.compile(gpu,flags=re.I))
        ]
        gpu_nospace = gpu.replace(' ','')
        df_with_gpu_name_nospace = target_df.loc[
            target_df['gpu_name'].str.contains(re.compile(gpu_nospace,flags=re.I))
        ]
        
        df_with_gpu_name = df_with_gpu_name.copy()
        df_with_gpu_name['gpu_unit_name'] = gpu_brand + ' ' +gpu
        gpu_base_name_df = pd.concat([gpu_base_name_df,df_with_gpu_name,df_with_gpu_name_nospace])
        gpu_base_name_df.drop_duplicates(subset='retail_url',keep='last',inplace=True)
    
    return gpu_base_name_df