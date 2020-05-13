from typing import List

import pymongo

from config import CONFIG
from result import Result


class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient(CONFIG["mongodb"]["connection_string"])
        self.cursor = self.client.get_database("immobilien").get_collection("frankfurt")

    def insert(self, documents: List[Result]) -> None:
        self.cursor.insert_many(documents)
