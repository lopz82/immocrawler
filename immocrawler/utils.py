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


def extract_city(s: str) -> str:
    s = s.rsplit(",", maxsplit=1)[0]
    return s.split(" ", maxsplit=1)[1]


def extract_neighborhood(s: str) -> str:
    return s.rsplit(",")[-1].strip()


def extract_zip_code(s: str) -> int:
    return int(s.split(" ")[0])
