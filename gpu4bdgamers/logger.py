import logging
from gpu4bdgamers.dirs import LOGS_DIR

import pathlib

def setup_logging(
        log_filename:str,
        log_dir:pathlib.Path = LOGS_DIR,
) -> logging.RootLogger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_dir/log_filename,mode="a+"),
            logging.StreamHandler()
        ]
    )

    return logging