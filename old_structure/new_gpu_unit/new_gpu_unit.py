from exceptions import GPUAlreadyExistsError, InvalidGpuUnitFormatError

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


def add_to_excel(
        gpu_unit_name:str,
        filename:str,
        sheet_name:str=EXCEL_SHEET_NAME,
) -> None:
    """Adds gpu unit to the excel file."""
    pass