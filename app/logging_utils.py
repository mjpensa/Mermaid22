import logging
import json
from typing import Any

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def log_structured(logger: logging.Logger, level: int, message: str, **kwargs: Any):
    log_entry = {"message": message, **kwargs}
    logger.log(level, json.dumps(log_entry))