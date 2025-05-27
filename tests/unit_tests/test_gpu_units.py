from gpu4bdgamers.data_coll_script import read_gpu_from_files
from gpu4bdgamers.naming import add_gpu_unit_name

import pandas as pd

FILE_FOR_TEST = "gpu_units_test.txt"

def test_no_empty_str_read_gpu_from_files(
    filename:str = FILE_FOR_TEST
) -> None:
    """Test to check no empty strings are present in the list of gpu's
    when read from files"""
    gpu_list = read_gpu_from_files(filename)
    assert "" not in gpu_list


def test_add_gpu_unit_name_default(
        master_df_test:pd.DataFrame,
        radeon_gpu_list:list[str],
        geforce_gpu_list:list[str],
        intel_gpu_list:list[str],
        gpu_unit_index:dict[str, dict[str, list[int]]]
) -> None:
    """Test the default behavior of add_gpu_unit - checks if it can 
    identify the gpu units from gpu names (according to the behavior of the
    first iteration of gpu4bdgamers)"""
    # need to specify index, else reading all rows and assigning the 
    # gpu_unit_name to nan
    master_df_test_with_space = master_df_test[:18]

    radeon_df = add_gpu_unit_name(master_df_test_with_space,radeon_gpu_list,"Radeon")
    geforce_df = add_gpu_unit_name(master_df_test_with_space,geforce_gpu_list,"Geforce")
    intel_df = add_gpu_unit_name(master_df_test_with_space,intel_gpu_list,"Intel")

    for gpu_unit_name,index_list in gpu_unit_index['Radeon'].items():
        for i in index_list:
            gpu_name:str = master_df_test_with_space.gpu_name.iloc[i]
            assert radeon_df['gpu_unit_name'][
                radeon_df['gpu_name']==gpu_name
            ].iloc[0] == gpu_unit_name
    
    for gpu_unit_name,index_list in gpu_unit_index['Geforce'].items():
        for i in index_list:
            gpu_name:str = master_df_test_with_space.gpu_name.iloc[i]
            assert geforce_df['gpu_unit_name'][
                geforce_df['gpu_name']==gpu_name
            ].iloc[0] == gpu_unit_name
    
    for gpu_unit_name,index_list in gpu_unit_index['Intel'].items():
        for i in index_list:
            gpu_name:str = master_df_test_with_space.gpu_name.iloc[i]
            assert intel_df['gpu_unit_name'][
                intel_df['gpu_name']==gpu_name
            ].iloc[0] == gpu_unit_name

def test_add_gpu_unit_name_gpu_name_nospace(
        master_df_test:pd.DataFrame,
        radeon_gpu_list:list[str],
        geforce_gpu_list:list[str],
        intel_gpu_list:list[str],
) -> None:
    """Test to check add_gpu_unit_name can correctly identify gpu units
    from gpu names, within which the gpu unit part has no space within it
    e.g. RTX2060"""
    master_df_test_nospace = master_df_test.iloc[18:26]
    
    radeon_df_nospace = add_gpu_unit_name(
        master_df_test_nospace,radeon_gpu_list,"Radeon"
    )
    geforce_df_nospace = add_gpu_unit_name(
        master_df_test_nospace,geforce_gpu_list,"Geforce"
    )
    intel_df_nospace = add_gpu_unit_name(
        master_df_test_nospace,intel_gpu_list,"Intel"
    )

    radeon_gpu_series = ["Radeon RX 580","Radeon RX 7600","Radeon RX 7600 XT"]
    geforce_gpu_series = ["Geforce RTX 2060","Geforce RTX 4060","Geforce RTX 4060 Ti"]
    intel_gpu_series = ["Intel Arc A750","Intel Arc A770"]

    for i in range(3):

        assert radeon_df_nospace['gpu_unit_name'].iloc[i] == radeon_gpu_series[i]
        
        assert geforce_df_nospace['gpu_unit_name'].iloc[i] == geforce_gpu_series[i]
        
        if i<=1:
            assert intel_df_nospace['gpu_unit_name'].iloc[i] == intel_gpu_series[i]

