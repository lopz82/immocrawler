import requests
from bs4 import BeautifulSoup

from config import BASE_URL, CRITERIA, MAIN_LINK


class Search:

    def __init__(self):
        self.url = "https://www.immobilienscout24.de/Suche/de/hessen/frankfurt-am-main/wohnung-mieten?enteredFrom=one_step_search"
        self.soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        self.tasks = None
        self.pages = None

    def parse(self):
        links = self.soup.select(MAIN_LINK)
        self.tasks = [
            SpecialResult(a["href"]) if a["href"].startswith("https://") else StandardResult(BASE_URL + a["href"]) for a
            in links]

    def get_pages(self):
        self.pages = len(self.soup.select("div#pageSelection select.select option"))


class SpecialResult:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def extract_data(self):
        pass


class StandardResult:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def extract_data(self):
        html = requests.get(self.url).content
        soup = BeautifulSoup(html, "html.parser")
        for section, CSS_selector in CRITERIA.items():
            item = soup.select(CSS_selector)
            assert len(item) == 1
            self.data[section] = item[0].get_text()


s = Search()
s.get_pages()
s.parse()
pass
