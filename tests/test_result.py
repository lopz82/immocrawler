from unittest.mock import patch

import pytest

from immocrawler.result import Result
from tests.stubs import Date
from tests.test_data import R1, R2, R3


@pytest.mark.skip("datetime.now needs to be mocked")
@pytest.mark.parametrize("url, kwargs", [
    ("http://fake.url", R1)
])
@patch("immocrawler.result.datetime")
@patch("immocrawler.result.Result.generate_sha256")
@patch("immocrawler.result.Result.geolocate")
def test_result_init(mock_geolocate, mock_sha256, mock_datetime_now, url, kwargs):
    fake_date = Date(1982, 7, 16, 18, 0, 0)
    mock_datetime_now.return_value = fake_date

    r = Result(url, **kwargs)

    assert r.url == url
    for key, value in kwargs.items():
        assert getattr(r, key) == value
    assert r.sha256 is None
    assert r.longitude is None
    assert r.latitude is None
    assert r.date == fake_date
    assert mock_geolocate.call_count == 1
    assert mock_sha256.call_count == 1


@pytest.mark.parametrize("url, kwargs", [
    ("http://fake.url", R1),
    ("http://fake.url", R2),
    ("http://fake.url", R3)

])
# Patching geolocate to avoid being called. Using a print instead (It is not expensive and useless)
@patch.object(Result, "geolocate", print)
def test_generate_sha256(url, kwargs):
    r = Result(url, **kwargs)
    assert len(r.sha256) == 64


@patch("immocrawler.result.geolocation")
def test_geolocate(mock_geolocation):
    mock_geolocation.return_value = 1, 2
    r = Result("http://fake.url", **R1)
    assert r.address is not None
    assert r.zip_city_neighborhood is not None
    assert mock_geolocation.call_count == 1
    assert mock_geolocation.call_args.args == (f"{R1['address']} {R1['zip_city_neighborhood']}",)
    assert r.latitude == 1
    assert r.longitude == 2


# Patching geolocate to avoid being called. Using a print instead (It is not expensive and useless)
@patch.object(Result, "geolocate", print)
def test_result_repr_():
    r = Result("http://fake.url", **R1)
    assert r.__repr__() == "Result(http://fake.url)"


@pytest.mark.skip("datetime.now needs to be mocked")
@patch("immocrawler.result.datetime")
@patch("immocrawler.result.Result.geolocate")
@patch("immocrawler.result.Result.generate_sha256")
def test_result_data_property(mock_sha256, mock_geolocation, mock_datetime_now):
    sha256 = "f0af17449a83681de22db7ce16672f16f37131bec0022371d4ace5d1854301e0"
    latlong = (1.23, 4.56)
    fake_date = Date(1982, 7, 16, 18, 0, 0)
    mock_sha256.return_value = sha256
    mock_geolocation.return_value = latlong
    mock_datetime_now.return_value = fake_date

    r = Result("http://fake.url", **R1)
    assert r.data == {**R1, "sha256": sha256, "latitude": 1.23, "longitude": 4.56, "date": fake_date, "zip_code": 60528,
                      "city": "Frankfurt am Main", "neighborhood": "Niederrad"}
