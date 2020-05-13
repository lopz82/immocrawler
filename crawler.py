import logging
import random
import sys
from time import sleep
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from config import BASE_URL, MAIN_LINK, PAGE_NUMBER_SLUG, HEADERS
from db import MongoDB
from result import Result
from tasks import SpecialSearchTask, StandardSearchTask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)


class Search:
    def __init__(self, wait: Tuple[int] = None, rooms: int = None, price: float = None,
                 living_space: float = None) -> None:
        self.cursor = MongoDB()
        self.rooms = rooms
        self.price = price
        self.living_space = living_space
        self.url = BASE_URL + self.add_params_to_url()
        self.soup = Search.crawl(self.url)
        self.tasks = []
        self.n_pages = None
        self.wait = (5, 10) or tuple(wait)  # Long wait to fake human behaviour
        self.results = []
        self.result_pages = []

    def insert(self, documents: List[Result]) -> None:
        self.cursor.insert(documents)

    def add_params_to_url(self) -> str:
        params = [""]
        if self.rooms:
            params.append(f"numberofrooms={self.rooms}")
        if self.price:
            params.append(f"price=-{self.price}")
        if self.living_space:
            params.append(f"livingspace={self.living_space}")
        return "/Suche/de/hessen/frankfurt-am-main/wohnung-mieten?" + "&".join(params)

    @staticmethod
    def crawl(url) -> BeautifulSoup:
        log.info(f"Crawling {url}")
        return BeautifulSoup(Search.request_get(url), "html.parser")

    @staticmethod
    def request_get(url: str) -> bytes:
        try:
            return requests.get(url, headers=HEADERS).content
        except requests.exceptions.RequestException as ex:
            log.error(f"Error after GET request to {url}: {ex}")

    @property
    def random_time(self) -> int:
        random_time = random.randint(*self.wait)
        log.info(f"Generated random time: {random_time} s.")
        return random_time

    def shuffle_result_pages(self) -> None:
        random.shuffle(self.result_pages)

    def shuffle_tasks(self) -> None:
        random.shuffle(self.tasks)

    def get_pages_num(self) -> None:
        self.n_pages = len(self.soup.select("div#pageSelection select.select option"))
        log.info(f"Number of pages: {self.n_pages}")

    def collect_result_pages_urls(self) -> None:
        self.get_pages_num()
        log.info("Collecting result pages...")
        if self.n_pages > 0:
            self.result_pages.extend([self.url + PAGE_NUMBER_SLUG.format(n) for n in range(1, self.n_pages + 1)])
        else:
            self.result_pages.append(self.url)
        log.info(f"{len(self.result_pages)} pages collected.")

    def collect_tasks(self) -> None:
        self.collect_result_pages_urls()
        # self.shuffle_result_pages()
        for url in self.result_pages:
            log.info(f"Collecting tasks for {url}")
            self.create_tasks_from_url(url)

    def create_tasks_from_url(self, url: str) -> None:
        sleep(self.random_time)
        log.info(f"Crawling {url}.")
        html = Search.crawl(url)
        log.info(f"Extracting links from CSS selector.")
        links = html.select(MAIN_LINK)
        log.info(f"{len(links)} links found.")
        tasks = [SpecialSearchTask(a["href"]) if a["href"].startswith("https://") else StandardSearchTask(
            BASE_URL + a["href"])
                 for a in links]
        self.tasks.extend(tasks)
        log.info(f"Added {len(tasks)} new tasks")
        log.debug(f"Added {tasks}")

    def run_tasks(self) -> None:
        # self.shuffle_tasks()
        log.info("Running tasks.")
        for task in self.tasks:
            wait = self.random_time
            log.info(f"Waiting {wait} seconds.")
            sleep(wait)
            log.info(f"Running {task}.")
            try:
                self.results.append(task.run())
            except ValueError as exc:
                log.error(f"Exception thrown running {task}: {exc}")
            log.info(f"Task ran successfully.")

    def insert_results(self) -> None:
        documents = [result.data for result in self.results]
        self.insert(documents)

    def run(self) -> None:
        self.collect_tasks()
        self.run_tasks()
        self.insert_results()
