from typing import Type, TypeVar

import requests
from bs4 import BeautifulSoup

from config import CRITERIA, HEADERS, BASE_URL
from result import Result
from utils import get_logger

log = get_logger(__name__)


class SearchTask:
    def __init__(self, url: str) -> None:
        self.url = url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.url})"


class SpecialSearchTask(SearchTask):
    def __init__(self, url: str) -> None:
        super(SpecialSearchTask, self).__init__(url)

    def run(self):
        pass


class StandardSearchTask(SearchTask):
    def __init__(self, url: str) -> None:
        super(StandardSearchTask, self).__init__(BASE_URL + url)

    def run(self) -> Result:
        data = {}
        soup = self._get_html()
        image_source = soup.select("div.first-gallery-picture-container img")
        if len(image_source) == 1:
            data["image"] = image_source[0].get("src", "Not found")
        else:
            log.error(
                f"Error extracting image with div.first-gallery-picture-container img. Expecting one result, got {len(image_source)}.")
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

    def _get_html(self) -> BeautifulSoup:
        log.info(f"Crawling {self.url}.")
        html = requests.get(self.url, headers=HEADERS).content
        soup = BeautifulSoup(html, "html.parser")
        return soup


Task = TypeVar("Task", bound=SearchTask)


class SearchTaskFactory:
    @classmethod
    def new_task(cls, url: str) -> Type[Task]:
        if cls.is_special_task(url):
            return SpecialSearchTask(url)
        else:
            return StandardSearchTask(url)

    @staticmethod
    def is_special_task(url: str) -> bool:
        return url.startswith("https://")
