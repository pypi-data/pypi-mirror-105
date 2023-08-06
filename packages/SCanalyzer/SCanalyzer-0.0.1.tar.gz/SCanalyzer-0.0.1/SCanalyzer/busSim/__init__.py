from .busSim import BusSim
from .config import Config

import logging
import sys

LOG_FILE_PATH = "busSim.log"


def _init_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    # init file handler
    handler = logging.FileHandler(LOG_FILE_PATH)
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


_init_logger()
