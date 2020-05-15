from datetime import datetime
from hashlib import sha256

from geo import geolocation


class Result:
    def __init__(self, url, **kwargs):
        self.__dict__.update(**kwargs)
        self.sha256 = self.generate_sha256()
        self.url = url
        self.date = datetime.now()
        self.latitude = None
        self.longitude = None
        self.geolocate()

    def generate_sha256(self):

        self.sha256 = sha256(str(self.__dict__).encode()).hexdigest()

    def geolocate(self):
        assert (getattr(self, "address"))
        assert (getattr(self, "zip_city_neighborhood"))
        if self.address and self.zip_city_neighborhood:
            self.latitude, self.longitude = geolocation(f"{self.address} {self.zip_city_neighborhood}")

    def __repr__(self):
        return f"{__class__.__name__} {self.url}"

    def __str__(self):
        return str(self.__dict__)

    @property
    def data(self):
        return self.__dict__
