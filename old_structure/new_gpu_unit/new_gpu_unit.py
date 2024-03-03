# TODO:
#       - add gpu unit to one of the gpu_units_of_interest/ files
#       - a check to see if the gpu unit already exists
#       - add to excel file
#       - check if already exists
#       - push to db
#       - check if already exists

# CONFIGS
GPU_UNITS_OF_INTEREST_DIR = "../gpu_units_of_interest"
GEFORCE_GPU_UNITS_OF_INTEREST_FILE = "geforce_gpu_units.txt"



class GPUAlreadyExistsError(Exception):
    def __init__(self, gpu_name:str, filename:str):
        self.gpu_name = gpu_name
        self.filename = filename
        super().__init__(f"{gpu_name} already exists in file {filename}")


def _check_if_exists_gpu_units_of_interest_file(
        gpu_unit:str,
        filename:str,
) -> bool:
    """Checks if a particular gpu unit exists in a
    particular file name"""
    with open(filename,"r") as reader:
        gpu_units = reader.read()
        gpu_unit_list = gpu_units.splitlines()

    if gpu_unit in gpu_unit_list:
        return True
    else:
        return False


def add_to_gpu_units_of_interest_file(
        gpu_unit:str,
        full_filename:str,
) -> None:
    """Adds a new gpu unit to the appropriate file"""
    if _check_if_exists_gpu_units_of_interest_file(gpu_unit,full_filename):
        raise GPUAlreadyExistsError
    
    else:
        with open(full_filename,"a") as gpu_unit_writer:
            gpu_unit_writer.write(f"\n{gpu_unit}")
