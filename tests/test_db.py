from unittest.mock import MagicMock

import pytest
from pymongo import MongoClient
from pymongo.collection import Collection

from immocrawler.db import MongoDB
from tests.stubs import Result


@pytest.fixture(scope="function")
def mongodb():
    return MongoDB()


def test_mongodb_init(mongodb):
    assert isinstance(mongodb.client, MongoClient)
    assert isinstance(mongodb.cursor, Collection)


def test_mongodb_save(mongodb):
    mongodb.cursor = MagicMock(autospec=True)
    mongodb.cursor.insert = MagicMock(autospec=True)

    res = Result(content={"fake": "data"})
    mongodb.save(res)

    assert mongodb.cursor.insert.call_count == 1
    assert mongodb.cursor.insert.call_args.args == ({"fake": "data"},)
