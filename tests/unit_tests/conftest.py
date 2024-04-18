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
def gpu_unit_index() -> dict[str,list[int]]:
    return {
        "RX 580": [0],
        "RX 7600": [1],
        "RX 7600 XT": [2],
        "RX 6900 XT": [3,4],
        "GTX 1650": [5,6],
        "RTX 2060": [7],
        "RTX 2080 Super": [8],
        "RTX 4060": [9,10],
        "RTX 4060 Ti": [11,12],
        "RTX 3070": [13],
        "Arc A580": [14],
        "Arc A750": [15,16],
        "Arc A770": [17],
    }