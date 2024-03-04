from exceptions import GPUAlreadyExistsError, InvalidGpuUnitFormatError

import pandas as pd
# TODO:
#       -check to see if input format is valid
#       - add to excel file
#       - check if already exists
#       - push to db
#       - check if already exists

# CONFIGS
GPU_UNITS_OF_INTEREST_DIR = "../gpu_units_of_interest"
GEFORCE_GPU_UNITS_OF_INTEREST_FILE = "geforce_gpu_units.txt"

EXCEL_SHEET_NAME = "tier_score_sheet"


def _check_gpu_unit_name_valid_input(gpu_unit_name:str) -> bool:
    """Checks if the gpu_unit_name is formatted correctly. Else,
    InvalidGpuUnitFormatError is raised."""
    pass


def input_gpu_unit_name(gpu_unit_name:str) -> str:
    # TODO: - tie the filename to the gpu_unit 
    #       (e.g. if RTX|GTX then geforce file etc.)
    #       - add test to see if this is being ensured
    pass


def auto_add_details_to_gpu_unit(gpu_unit_name:str) -> pd.DataFrame:
    """To create a series out of a gpu_unit_name, where it will
    automatically assign the correct prefix e.g. Radeon for RX GPU's,
    GeForce for RTX/GTX GPU's, and so on, as well as adds performance values,
    launch prices and so on"""
    # assigning correct prefixes should probably be a separate internal function

def add_to_excel(
        gpu_unit_name:str,
        filename:str,
        sheet_name:str=EXCEL_SHEET_NAME,
) -> None:
    """Adds gpu unit to the excel file."""
    # should contain functionality for automatically adding brand prefix
    # e.g. GeForce, Radeon, and Intel
    # should also contain functionality to automatically add some comment codes
    # based on some naming convention
    # this probably should be a separate function
    pass