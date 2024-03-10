import logging

def setup_logging() -> logging.RootLogger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("./logs/gpu_data_coll_script.log",mode="a+"),
            logging.StreamHandler()
        ]
    )

    return logging