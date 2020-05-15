import logging
import random
import sys


def get_logger(name: str):
    log = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


log = get_logger(__name__)


def random_time(wait) -> int:
    time = random.randint(*wait)
    log.info(f"Generated random time: {time} s.")
    return time
