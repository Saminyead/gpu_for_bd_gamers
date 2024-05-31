import pathlib
import os

PROJECT_ROOT = pathlib.Path(os.getenv('PROJECT_ROOT',pathlib.Path(__file__).parent)) 

CONFIGS_DIR = PROJECT_ROOT/'configs'
SCRAPING_CONFIG_FILE = CONFIGS_DIR/'scraping_config.toml'

LOGS_DIR = PROJECT_ROOT/'logs'

GPU_DATA_EXCEL_FILE = PROJECT_ROOT/'tier_score.xlsx'

GPU_UNITS_LIST_DIR = PROJECT_ROOT/'gpu_units_of_interest'
GEFORCE_UNITS_FILE = GPU_UNITS_LIST_DIR/'geforce_gpu_units.txt'
RADEON_UNITS_FILE = GPU_UNITS_LIST_DIR/'radeon_gpu_units.txt'
INTEL_UNITS_FILE = GPU_UNITS_LIST_DIR/'intel_gpu_units.txt'