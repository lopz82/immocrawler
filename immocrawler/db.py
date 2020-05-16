from pymongo import MongoClient

from immocrawler.config import CONFIG
from immocrawler.result import Result


class MongoDB:
    def __init__(self):
        self.client = MongoClient(CONFIG["mongodb"]["connection_string"])
        self.cursor = self.client.get_database("immobilien").get_collection("frankfurt")

    def save(self, result: Result) -> None:
        self.cursor.insert(result.data)
