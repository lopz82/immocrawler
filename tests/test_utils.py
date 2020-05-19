from logging import Logger

import pytest

from immocrawler.utils import get_logger, random_time, extract_city, extract_neighborhood, extract_zip_code


def test_get_logger():
    log = get_logger("fake")
    assert isinstance(log, Logger)
    assert log.name == "fake"


def test_random_time():
    wait = (5, 10)
    time = random_time(wait)
    assert wait[0] <= time <= wait[1]


@pytest.mark.parametrize("address, expected", [
    ("60594 Frankfurt am Main, Sachsenhausen-Nord", "Frankfurt am Main"),
    ("60431 Frankfurt, Ginnheim", "Frankfurt"),
    ("65929 Frankfurt am Main, Höchst", "Frankfurt am Main"),
    ("65936 Frankfurt, Sossenheim", "Frankfurt"),
])
def test_extract_city(address, expected):
    assert extract_city(address) == expected


@pytest.mark.parametrize("address, expected", [
    ("60594 Frankfurt am Main, Sachsenhausen-Nord", "Sachsenhausen-Nord"),
    ("60431 Frankfurt, Ginnheim", "Ginnheim"),
    ("65929 Frankfurt am Main, Höchst", "Höchst"),
    ("65936 Frankfurt, Sossenheim", "Sossenheim"),
])
def test_extract_neighborhood(address, expected):
    assert extract_neighborhood(address) == expected


@pytest.mark.parametrize("address, expected", [
    ("60594 Frankfurt am Main, Sachsenhausen-Nord", 60594),
    ("60431 Frankfurt, Ginnheim", 60431),
    ("65929 Frankfurt am Main, Höchst", 65929),
    ("65936 Frankfurt, Sossenheim", 65936),
])
def test_extract_zip_code(address, expected):
    assert extract_zip_code(address) == expected
