from gpu4bdgamers.data_coll_script import read_gpu_from_files
from gpu4bdgamers.gpu_units import add_gpu_unit_name

import pandas as pd

FILE_FOR_TEST = "gpu_units_test.txt"

def test_no_empty_str_read_gpu_from_files(
    filename:str = FILE_FOR_TEST
) -> None:
    gpu_list = read_gpu_from_files(filename)
    assert "" not in gpu_list


def test_add_gpu_unit_name(
        master_df_test:pd.DataFrame,
        radeon_gpu_list:list[str],
        geforce_gpu_list:list[str],
        intel_gpu_list:list[str],
        gpu_unit_index:dict[str, dict[str, list[int]]]
) -> None:
    radeon_df = add_gpu_unit_name(master_df_test,radeon_gpu_list,"Radeon")
    geforce_df = add_gpu_unit_name(master_df_test,geforce_gpu_list,"Geforce")
    intel_df = add_gpu_unit_name(master_df_test,intel_gpu_list,"Intel")

    for gpu_unit_name,index_list in gpu_unit_index['Radeon'].items():
        for i in index_list:
            gpu_name:str = master_df_test.gpu_name.iloc[i]
            assert radeon_df[
                radeon_df['gpu_name']==gpu_name
            ]['gpu_unit_name'].iloc[0] == gpu_unit_name
    
    for gpu_unit_name,index_list in gpu_unit_index['Geforce'].items():
        for i in index_list:
            gpu_name:str = master_df_test.gpu_name.iloc[i]
            assert geforce_df[
                geforce_df['gpu_name']==gpu_name
            ]['gpu_unit_name'].iloc[0] == gpu_unit_name
    
    for gpu_unit_name,index_list in gpu_unit_index['Intel'].items():
        for i in index_list:
            gpu_name:str = master_df_test.gpu_name.iloc[i]
            assert intel_df[
                intel_df['gpu_name']==gpu_name
            ]['gpu_unit_name'].iloc[0] == gpu_unit_name