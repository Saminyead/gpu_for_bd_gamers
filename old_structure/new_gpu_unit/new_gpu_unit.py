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


def _check_gpu_unit_name_valid_input(gpu_unit_name:str) -> bool:
    """Checks if the gpu_unit_name is formatted correctly. Else,
    InvalidGpuUnitFormatError is raised."""
    pass


def input_gpu_unit_name(gpu_unit_name:str) -> str:
    # TODO: - tie the filename to the gpu_unit 
    #       (e.g. if RTX|GTX then geforce file etc.)
    #       - add test to see if this is being ensured
    pass

def _check_does_not_exists_gpu_unit_of_interest_in_file(
        gpu_unit:str,
        filename:str,
) -> bool|Exception:
    """Checks if a particular gpu unit exists in a
    particular file name"""
    with open(filename,"r") as reader:
        gpu_units = reader.read()
        gpu_unit_list = gpu_units.splitlines()

    if gpu_unit in gpu_unit_list:
        raise GPUAlreadyExistsError(gpu_unit,filename)
    else:
        return True


def add_to_gpu_units_of_interest_file(
        gpu_unit:str,
        full_filename:str,
) -> None:
    """Adds a new gpu unit to the appropriate file""" 
    _check_does_not_exists_gpu_unit_of_interest_in_file(gpu_unit,full_filename)
    
    with open(full_filename,"a") as gpu_unit_writer:
        gpu_unit_writer.write(f"{gpu_unit}\n")
