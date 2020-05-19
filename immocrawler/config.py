import yaml

from immocrawler.cleanups import from_numeric, from_text


def read_config():
    with open("./immocrawler/connections.yml") as f:
        return yaml.safe_load(f)


CONFIG = read_config()
FILTER = {
    "text": from_text,
    "numeric": from_numeric,
    "address": from_text
}
BASE_URL = "https://www.immobilienscout24.de"
CRITERIA = {
    "title": {
        "selector": "div h1#expose-title",
        "kind": "text"},
    "address": {
        "selector": "span[data-qa] div.address-block span:first-child",
        "kind": "address",
    },
    "zip_city_neighborhood": {
        "selector": "span[data-qa] div.address-block span.zip-region-and-country",
        "kind": "address",
    },
    "type": {
        "selector": "dd.is24qa-typ",
        "kind": "text"
    },
    "floor": {
        "selector": "dd.is24qa-etage",
        "kind": "text"
    },
    "surface": {
        "selector": "dd.is24qa-wohnflaeche-ca",
        "kind": "numeric"
    },
    "available_from": {
        "selector": "dd.is24qa-bezugsfrei-ab",
        "kind": "text"
    },
    "rooms": {
        "selector": "dd.is24qa-zimmer",
        "kind": "numeric"
    },
    "sleeping_rooms": {
        "selector": "dd.is24qa-schlafzimmer",
        "kind": "numeric"
    },
    "restrooms": {
        "selector": "dd.is24qa-badezimmer",
        "kind": "numeric"
    },
    "pets": {
        "selector": "dd.is24qa-haustiere",
        "kind": "text"
    },
    "garage": {
        "selector": "dd.is24qa-garage-stellplatz",
        "kind": "text"
    },
    "rent": {
        "selector": "dd.is24qa-kaltmiete",
        "kind": "numeric"
    },
    "side_costs": {
        "selector": "dd.is24qa-nebenkosten",
        "kind": "numeric"
    },
    "heating": {
        "selector": "dd.is24qa-heizkosten",
        "kind": "text"
    },
    "deposit": {
        "selector": "div.is24qa-kaution-o-genossenschaftsanteile",
        "kind": "text"
    },
    "rent_for_garage": {
        "selector": "dd.is24qa-miete-fuer-garagestellplatz",
        "kind": "numeric",
    },
    "construction_year": {
        "selector": "dd.is24qa-baujahr",
        "kind": "text"
    },
    "status": {
        "selector": "dd.is24qa-objektzustand",
        "kind": "text"
    },
    "heating_type": {
        "selector": "dd.is24qa-heizungsart",
        "kind": "text"
    },
    "description": {
        "selector": "pre.is24qa-objektbeschreibung",
        "kind": "text"
    },
    "equipment": {
        "selector": "pre.is24qa-ausstattung",
        "kind": "text"
    },
}

MAIN_LINK = "a.result-list-entry__brand-title-container"
# MAIN_LINK = "div.result-list-entry__data a.result-list-entry__brand-title-container"
PAGE_NUMBER_SLUG = "?pagenumber={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}
