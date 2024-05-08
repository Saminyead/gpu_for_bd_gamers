import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()

CONFIGS_DIR = PROJECT_ROOT/'configs'
SCRAPING_CONFIG_FILE = CONFIGS_DIR/'scraping_config.toml'
