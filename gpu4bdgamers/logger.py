import logging
from gpu4bdgamers.dirs import LOGS_DIR

def setup_logging(log_dir = LOGS_DIR) -> logging.RootLogger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOGS_DIR/"gpu_data_coll_script.log",mode="a+"),
            logging.StreamHandler()
        ]
    )

    return logging