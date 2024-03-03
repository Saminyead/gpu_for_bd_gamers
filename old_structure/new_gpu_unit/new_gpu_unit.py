# TODO:
#       - add gpu unit to one of the gpu_units_of_interest/ files
#       - a check to see if the gpu unit already exists
#       - add to excel file
#       - check if already exists
#       - push to db
#       - check if already exists

class GPUAlreadyExistsError(Exception):
    def __init__(self, gpu_name:str, filename:str):
        self.gpu_name = gpu_name
        self.filename = filename
        super().__init__(f"{gpu_name} already exists in file {filename}")


def _check_if_exists_gpu_units_of_interest_file(
        filename:str,
        gpu_unit:str
) -> bool:
    pass


def add_to_gpu_units_interest_file(
        filename:str,
        gpu_unit:str
) -> None:
    pass