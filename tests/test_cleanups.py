import pytest

from immocrawler.cleanups import from_numeric, from_text, from_numeric


@pytest.mark.parametrize("string, expected", [
    (" 800 € ", 800),
    ("800€", 800),
    ("\t\n800 €", 800),
    ("\t\n800 €\t\n", 800),
    (" + 190 € ", 190),
    (" + 190€ ", 190),
    ("+ 266,80 €", 266.80),
    ("1.355€", 1355),
    ("1.355 €", 1355),
    ("4.065,00", 4065),
    ("4.065,00€", 4065),
    ("4.065,00 €", 4065),
    (" 107 m² ", 107),
    (" 1 ", 1),
    ("\n\t107 m²\n\t", 107),
    ("\n\t2\n\t ", 2),
    ("23,45", 23.45),
])
def test_from_numeric(string, expected):
    assert from_numeric(string) == expected


@pytest.mark.parametrize("string, expected", [
    (" Penthouse ", "Penthouse"),
    ("\tPenthouse\t", "Penthouse"),
    (" \nPenthouse\n", "Penthouse"),
])
def test_from_text(string, expected):
    assert from_text(string) == expected

