from exceptions import GPUAlreadyExistsError


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