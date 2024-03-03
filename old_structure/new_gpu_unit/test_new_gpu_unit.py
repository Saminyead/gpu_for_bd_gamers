import pytest

from new_gpu_unit import add_to_gpu_units_of_interest_file, input_gpu_unit_name
from exceptions import GPUAlreadyExistsError, InvalidGpuUnitFormatError

TEST_DATA_DIR:str = "./test_data_dir"
EXISTS_FILE:str = "exists.txt"
DOES_NOT_EXIST_FILE:str = "not_exist.txt"

GPU_UNITS_EXISTING:list[str] = [
    "RX 6950 XT",
    "RTX 4070",
    "Arc A770"
]

GPU_UNITS_NOT_EXISTING:list[str] = [
    "RX 6900 XT",
    "RTX 4070 Ti",
    "Arc A380"
]


def _create_gpu_units_of_interest_test_file(
        filedir:str = f"{TEST_DATA_DIR}/{EXISTS_FILE}",
        gpu_units_of_interest_list:list[str] = GPU_UNITS_EXISTING
    ) -> str:
    """Creates a file with a number of gpu units for the
    tests"""
    
    with open(filedir,mode="w",encoding="utf-8") as writer:
        for gpu_unit in gpu_units_of_interest_list:
            writer.write(f"{gpu_unit}\n")

    return filedir


def test_does_not_add_to_existing_add_to_gpu_units_of_interest_file(
        gpu_unit_of_interest_list:list[str] = GPU_UNITS_EXISTING,
) -> None:
    """Checks if add_unit_to_gpu_units_of_interests_file checks if
    a gpu unit already exists in the file"""
    filedir = _create_gpu_units_of_interest_test_file()

    for gpu_unit in gpu_unit_of_interest_list:
        with pytest.raises(GPUAlreadyExistsError):
            add_to_gpu_units_of_interest_file(
                full_filename=filedir,
                gpu_unit=gpu_unit
            )


def test_adding_to_file_add_to_gpu_units_of_interest_file(
        filename:str = f"{TEST_DATA_DIR}/{DOES_NOT_EXIST_FILE}",
        gpu_units_of_interest_list:list[str] = GPU_UNITS_NOT_EXISTING
) -> None:
    """Checks if gpu unit names are being properly added to
    the gpu_units_of_interest file"""
    _create_gpu_units_of_interest_test_file(
        filedir=filename,
        gpu_units_of_interest_list=[]
    )

    for gpu_unit in gpu_units_of_interest_list:
        add_to_gpu_units_of_interest_file(gpu_unit,filename)
        
    with open(filename,'r') as gpu_units_reader:
        gpu_units = gpu_units_reader.read()
        gpu_units_list = gpu_units.splitlines()

    assert gpu_units_of_interest_list == gpu_units_list


# This should be for a different function, not 
# add_to_gpu_units_of_interest_file, this should just be for the 
# input function you will use in main
def test_input_format_is_valid_input_gpu_unit_name() -> None:
    """Checks if the format of the gpu_unit_name input is valid"""

    with pytest.raises(InvalidGpuUnitFormatError):
        input_gpu_unit_name("Not even a GPU name")
    
    with pytest.raises(InvalidGpuUnitFormatError):
        input_gpu_unit_name("GeForce RTX 3060")
