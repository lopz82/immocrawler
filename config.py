import yaml

CONFIG = None

with open("./connections.yml") as f:
    CONFIG = yaml.safe_load(f)

BASE_URL = "https://www.immobilienscout24.de"
CRITERIA = {
    "title": "div h1#expose-title",
    "address": "span[data-qa] div.address-block span:first-child",
    "zip_city_neighborhood": "span[data-qa] div.address-block span.zip-region-and-country",
    # "rent": "div.is24qa-kaltmiete",
    # "rooms": "div.is24qa-zi",
    # "surface": "div.is24qa-flaeche",
    "type": "dd.is24qa-typ",
    "floor": "dd.is24qa-etage",
    "surface": "dd.is24qa-wohnflaeche-ca",
    "available_from": "dd.is24qa-bezugsfrei-ab",
    "rooms": "dd.is24qa-zimmer",
    "sleeping_rooms": "dd.is24qa-schlafzimmer",
    "restrooms": "dd.is24qa-badezimmer",
    "pets": "dd.is24qa-haustiere",
    "garage": "dd.is24qa-garage-stellplatz",
    "rent": "dd.is24qa-kaltmiete",
    "side_costs": "dd.is24qa-nebenkosten",
    "heating": "dd.is24qa-heizkosten",
    "deposit": "div.is24qa-kaution-o-genossenschaftsanteile",
    "rent_for_garage": "dd.is24qa-miete-fuer-garagestellplatz",
    "construction_year": "dd.is24qa-baujahr",
    "status": "dd.is24qa-objektzustand",
    "heating_type": "dd.is24qa-heizungsart",
    "description": "pre.is24qa-objektbeschreibung",
    "equipment": "pre.is24qa-ausstattung"
}
MAIN_LINK = "div.result-list-entry__data a.result-list-entry__brand-title-container"
PAGE_NUMBER_SLUG = "?pagenumber={}"
HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}


