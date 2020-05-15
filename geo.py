from typing import Tuple

import requests

from config import CONFIG
from utils import get_logger

URL = "https://geocode.search.hereapi.com/v1/geocode"
API_KEY = CONFIG["here"]["api_key"]

log = get_logger(__name__)


def geolocation(address: str) -> Tuple[float, float]:
    params = {"apikey": API_KEY, "q": address}
    data = requests.get(URL, params).json()
    return float(data['items'][0]['position']['lat']), float(data['items'][0]['position']['lng'])
