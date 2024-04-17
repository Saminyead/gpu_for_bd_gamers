from gpu4bdgamers.data_coll_script import read_gpu_from_files

FILE_FOR_TEST = "gpu_units_test.txt"

def test_no_empty_str_read_gpu_from_files(
    filename:str = FILE_FOR_TEST
):
    gpu_list = read_gpu_from_files(filename)
    assert "" not in gpu_list