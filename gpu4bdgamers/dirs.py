import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
CONFIGS_DIR = f"{PROJECT_ROOT}/configs"

SCRAPING_CONFIG_FILE = f"{CONFIGS_DIR}/scraping_config.toml"
