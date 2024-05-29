import pathlib
import os

PROJECT_ROOT = pathlib.Path(os.getenv('PROJECT_ROOT',pathlib.Path(__file__).parent)) 

CONFIGS_DIR = PROJECT_ROOT/'configs'
SCRAPING_CONFIG_FILE = CONFIGS_DIR/'scraping_config.toml'