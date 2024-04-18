import pytest
import pandas as pd


MASTER_DF_CSV_FILE = "master_df.csv"

@pytest.fixture
def radeon_gpu_list() -> list[str]:
    return ["RX 580", "RX 7600 XT",  "RX 6900 XT", "RX 7600"]

@pytest.fixture
def geforce_gpu_list() -> list[str]:
    return [
        "GTX 1650", 
        "RTX 2060", 
        "RTX 2080 Super", 
        "RTX 3070", 
        "RTX 4060 Ti"
        "RTX 4060"
    ]

@pytest.fixture
def intel_gpu_list() -> list[str]:
    return ["Arc A580", "Arc A750", "Arc A770"]

@pytest.fixture
def master_df_test(filename:str=MASTER_DF_CSV_FILE) -> pd.DataFrame:
    return pd.read_csv(filename)

@pytest.fixture
def gpu_unit_index() -> dict[str, dict[str, list[int]]]:
    return {
        "Radeon": {
            "Radeon RX 580": [0],
            "Radeon RX 7600": [1],
            "Radeon RX 7600 XT": [2],
            "Radeon RX 6900 XT": [3,4],
        },
        "Geforce":{
            "Geforce GTX 1650": [5,6],
            "Geforce RTX 2060": [7],
            "Geforce RTX 2080 Super": [8],
            "Geforce RTX 4060": [9,10],
            "Geforce RTX 4060 Ti": [11,12],
            "Geforce RTX 3070": [13],
        },
        "Intel":{
            "Intel Arc A580": [14],
            "Intel Arc A750": [15,16],
            "Intel Arc A770": [17],
        },
    }