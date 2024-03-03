import pytest

from new_gpu_unit import add_to_gpu_units_interest_file, GPUAlreadyExistsError

TEST_DATA_DIR:str = "./test_data_dir"
EXISTS_FILE:str = "exists.txt"

GPU_UNITS_EXISTING:list[str] = [
    "Radeon RX 6950 XT",
    "GeForce RTX 4070",
    "Arc A770"
]

GPU_UNITS_NOT_EXISTING:list[str] = [
    "Radeon RX 6900 XT",
    "GeForce RTX 4070 Ti",
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


def test_check_does_not_add_to_existing_add_to_gpu_units_of_interest_file(
        gpu_unit_of_interest_list:list[str] = GPU_UNITS_EXISTING,
) -> None:
    """Checks if add_unit_to_gpu_units_of_interests_file checks if
    a gpu unit already exists in the file"""
    # run add_to_gpu_units_interest_file(exists_file, gpu_unit)
    # see if gpu_unit exists in exists_file
    filedir = _create_gpu_units_of_interest_test_file()

    for gpu_unit in gpu_unit_of_interest_list:
        with pytest.raises(GPUAlreadyExistsError):
            add_to_gpu_units_interest_file(filename=filedir,gpu_unit=gpu_unit)