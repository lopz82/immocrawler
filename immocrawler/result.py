import hashlib
from datetime import datetime

from immocrawler.geo import geolocation
from immocrawler.utils import extract_zip_code, extract_city, extract_neighborhood


class Result:
    def __init__(self, url, **kwargs):
        self.__dict__.update(**kwargs)
        self.sha256 = None
        self.generate_sha256()
        if self.zip_city_neighborhood:
            self.zip_code = extract_zip_code(self.zip_city_neighborhood)
            self.city = extract_city(self.zip_city_neighborhood)
            self.neighborhood = extract_neighborhood(self.zip_city_neighborhood)
        self.url = url
        self.date = datetime.now()
        self.latitude = None
        self.longitude = None
        self.geolocate()


    def generate_sha256(self):
        self.sha256 = hashlib.sha256(str(self.__dict__).encode()).hexdigest()

    def geolocate(self):
        assert (getattr(self, "address"))
        assert (getattr(self, "zip_city_neighborhood"))
        if self.address and self.zip_city_neighborhood:
            self.latitude, self.longitude = geolocation(f"{self.address} {self.zip_city_neighborhood}")

    def __repr__(self):
        return f"{__class__.__name__}({self.url})"

    @property
    def data(self):  # pragma: no cover
        return self.__dict__
