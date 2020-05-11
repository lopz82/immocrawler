BASE_URL = "https://www.immobilienscout24.de"
CRITERIA = {
    "title": "div h1#expose-title",
    "address": "span[data-qa] div.address-block span:first-child",
    "zip-city-neighborhood": "span[data-qa] div.address-block span.zip-region-and-country",
    # "rent": "div.is24qa-kaltmiete",
    # "rooms": "div.is24qa-zi",
    # "surface": "div.is24qa-flaeche",
    "type": "dd.is24qa-typ",
    "floor": "dd.is24qa-etage",
    "aprox. surface": "dd.is24qa-wohnflaeche-ca",
    "available from": "dd.is24qa-bezugsfrei-ab",
    "rooms": "dd.is24qa-zimmer",
    "sleeping rooms": "dd.is24qa-schlafzimmer",
    "restrooms": "dd.is24qa-badezimmer",
    "pets": "dd.is24qa-haustiere",
    "garage": "dd.is24qa-garage-stellplatz",
    "rent": "dd.is24qa-kaltmiete",
    "side costs": "dd.is24qa-nebenkosten",
    "heating": "dd.is24qa-heizkosten",
    "deposit": "div.is24qa-kaution-o-genossenschaftsanteile",
    "rent for garage": "dd.is24qa-miete-fuer-garagestellplatz",
    "construction year": "dd.is24qa-baujahr",
    "status": "dd.is24qa-objektzustand",
    "heating type": "dd.is24qa-heizungsart",
    "description": "pre.is24qa-objektbeschreibung",
    "equipment": "pre.is24qa-ausstattung"
}
MAIN_LINK = "div.result-list-entry__data a.result-list-entry__brand-title-container"
