import logging
import sys

import requests
from bs4 import BeautifulSoup

from config import CRITERIA, HEADERS
from result import Result

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)


class SpecialSearchTask:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def run(self):
        pass


class StandardSearchTask:
    def __init__(self, url):
        self.url = url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.url})"

    def run(self) -> Result:
        data = {}
        soup = self.get_html()
        image_source = soup.select("div.first-gallery-picture-container img")
        if len(image_source) == 1:
            data["image"] = image_source[0].get("src", "Not found")
        else:
            log.error(f"Error extracting image with div.first-gallery-picture-container img. Expecting one result, got {len(image_source)}.")
        for section, CSS_selector in CRITERIA.items():
            log.info(f"Extracting {section} with {CSS_selector} selector.")
            item = soup.select(CSS_selector)
            if len(item) != 1:
                log.error(f"Error extracting {section} with {CSS_selector}. Expecting one result, got {len(item)}. "
                          f"Setting {section} to None")
                data[section] = None
                continue
            data[section] = item[0].get_text()
            log.info(f"Added {section}: {item[0].get_text()}")
        result = Result(self.url, **data)
        return result

    def get_html(self) -> BeautifulSoup:
        log.info(f"Crawling {self.url}.")
        html = requests.get(self.url, headers=HEADERS).content
        soup = BeautifulSoup(html, "html.parser")
        return soup
