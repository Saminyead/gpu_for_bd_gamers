import logging
from gpu4bdgamers.dirs import LOGS_DIR

import pathlib

def setup_logging(log_dir:pathlib.Path = LOGS_DIR) -> logging.RootLogger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_dir/"gpu_data_coll_script.log",mode="a+"),
            logging.StreamHandler()
        ]
    )

    return logging