from datetime import datetime
from hashlib import sha256
from geo import geolocation


class Result:
    def __init__(self, url, **kwargs):
        self.__dict__.update(**kwargs)
        self.url = url
        self.date = datetime.now()
        self.latitude = None
        self.longitude = None
        self.geolocate()
        self.sha256 = sha256(str(self.__dict__).encode()).hexdigest()

    def geolocate(self):
        assert(getattr(self, "address"))
        if self.address:
            self.latitude, self.longitude = geolocation(self.address)

    def __repr__(self):
        return f"{__class__.__name__} {self.url}"

    def __str__(self):
        return str(self.__dict__)

    @property
    def data(self):
        return self.__dict__
