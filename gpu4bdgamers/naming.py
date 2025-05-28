import pandas as pd
import re


def _check_string_in_string(pattern: str, larger_string: str) -> bool:
    """Check if a smaller string is contained within a larger string"""
    pattern_lower_nospace = pattern.lower().replace(" ", "")
    larger_string_lower_nospace = larger_string.lower().replace(" ", "")
    if pattern_lower_nospace in larger_string_lower_nospace:
        return True
    else:
        return False


def _check_gpu_unit_in_gpu_name(gpu_name: str, gpu_unit_name: str) -> bool:
    gpu_unit_name_last_word_space = gpu_unit_name.split()[-1] + " "

    if not _check_string_in_string(
        pattern=gpu_unit_name_last_word_space, larger_string=gpu_name
    ):
        return False

    if _check_string_in_string(gpu_unit_name, gpu_name):
        return True
    else:
        return False


def add_gpu_unit_name(
    target_df: pd.DataFrame, gpu_list: list[str], gpu_brand: str
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

    target_df = target_df.copy()
    for gpu in gpu_list:
        df_with_gpu_name = target_df.loc[
            target_df["gpu_name"].apply(_check_gpu_unit_in_gpu_name, gpu_unit_name=gpu)
        ]

        # to stop complaining about SettingWithCopyWarning
        df_with_gpu_name = df_with_gpu_name.copy()
        df_with_gpu_name["gpu_unit_name"] = gpu_brand + " " + gpu
        gpu_base_name_df = pd.concat([gpu_base_name_df, df_with_gpu_name])

        # because in case of naming variant, there will be two gpu's,
        # one without a name extension like Ti/Super/XT, and the latter
        # with it. The latter is correct and should be kept.
        gpu_base_name_df.drop_duplicates(subset="retail_url", keep="last", inplace=True)

    return gpu_base_name_df


def gddr5_vs_gddr6_1650(gpu_1650):
    """since there are both gddr5 and gddr6 versions of the GTX 1650 with significant performance difference,
    this function distinguishes between them (to be applied with the .apply() method in dataframe)
    Args:
        gpu_1650 (string): GTX 1650 gpu name (as listed on retailer website)
    Returns:
        string: "GTX 1650 GDDR6"/"GTX 1650 GDDR5"
    """
    # sometimes the retailer names have the full 'GDDR6'/'GDDR5' spelled out, sometimes it just has 'D6'/'D5' in the name
    regex_match = re.search(pattern="gddr6|d6", string=gpu_1650, flags=re.I)
    if bool(regex_match) == True:
        return "Geforce GTX 1650 GDDR6"
    else:
        return "Geforce GTX 1650 GDDR5"
