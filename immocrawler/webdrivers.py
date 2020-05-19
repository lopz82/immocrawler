import requests

from immocrawler.config import HEADERS
from immocrawler.utils import get_logger

log = get_logger(__name__)


class RequestsDriver:
    def __init__(self):
        self.session = requests.Session()

    def html_from(self, url: str) -> bytes:
        try:
            return self.session.get(url, headers=HEADERS).content
        except requests.exceptions.RequestException as ex:
            log.error(f"Error after GET request to {url}: {ex}")
