import random
from time import sleep
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup

from config import BASE_URL, HEADERS, PAGE_NUMBER_SLUG, MAIN_LINK
from utils import get_logger, random_time

log = get_logger(__name__)


class ImmobilienScoutSearch:
    def __init__(self, wait: Tuple[int] = None, rooms: int = None, price: float = None,
                 living_space: float = None) -> None:
        self.rooms = rooms
        self.price = price
        self.living_space = living_space
        self.url = BASE_URL + self.add_params_to_url()
        self.soup = ImmobilienScoutSearch.crawl(self.url)
        self.n_pages = None
        self.wait = (5, 10) or tuple(wait)  # Long wait to fake human behaviour
        self.target_links = []
        self.result_pages = []

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
        return BeautifulSoup(ImmobilienScoutSearch.request_get(url), "html.parser")

    @staticmethod
    def request_get(url: str) -> bytes:
        try:
            return requests.get(url, headers=HEADERS).content
        except requests.exceptions.RequestException as ex:
            log.error(f"Error after GET request to {url}: {ex}")

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

    def shuffle_result_pages(self) -> None:
        random.shuffle(self.result_pages)

    def collect_target_links(self) -> None:
        self.collect_result_pages_urls()
        self.shuffle_result_pages()
        for url in self.result_pages:
            log.info(f"Collecting tasks for {url}")
            self.get_target_links_from(url)

    def get_target_links_from(self, url: str) -> None:
        sleep(random_time(self.wait))
        log.info(f"Crawling {url}.")
        html = ImmobilienScoutSearch.crawl(url)
        log.info(f"Extracting links from CSS selector.")
        soup = html.select(MAIN_LINK)
        links = [match["href"] for match in soup]
        log.info(f"{len(links)} links found.")
        self.target_links.extend(links)
        log.info(f"Added {len(links)} new links")
        log.debug(f"Added {links}")

    def run(self) -> List[str]:
        self.collect_target_links()
        return self.target_links
