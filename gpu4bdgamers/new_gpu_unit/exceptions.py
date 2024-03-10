class GPUAlreadyExistsError(Exception):
    def __init__(self, gpu_unit_name:str, filename:str):
        self.gpu_unit_name = gpu_unit_name
        self.filename = filename
        super().__init__(f"{gpu_unit_name} already exists in file {filename}")


class InvalidGpuUnitFormatError(Exception):
    def __init__(self, gpu_unit_name:str) -> None:
        super().__init__(f"""The name {gpu_unit_name} is not a valid 
                         GPU unit name. Please use the following format:
                         - 'RTX ****'/'GTX ****' for GeForce GPUs
                         - 'RX ****' for Radeon GPUs
                         - 'Arc ****' for Arc GPUs
                         If there has been a new release lineups, then please
                         change the _check_gpu_unit_name_valid_input function
                         in the new_gpu_unit module""")