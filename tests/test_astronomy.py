from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_astronomy_sun import astronomy_sun
from src.qweather_client.api_astronomy_moon import astronomy_moon
from src.qweather_client.api_astronomy_solar_elevation import astronomy_solar_elevation
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_astronomy_sun(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/astronomy/sun",
        json={"code": "200", "sunrise": "06:58", "sunset": "16:59"},
        status=200,
    )
    data = astronomy_sun(client, location="101010100", date="20210220")
    assert data["code"] == "200"


def test_astronomy_sun_invalid_date(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_sun(client, location="101010100", date="2021/02/20")


def test_astronomy_sun_missing_location(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_sun(client, location="", date="20210220")


@responses.activate
def test_astronomy_sun_with_lang(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/astronomy/sun",
        json={"code": "200", "sunrise": "06:58", "sunset": "16:59"},
        status=200,
    )
    data = astronomy_sun(client, location="101010100", date="20210220", lang="en")
    assert data["code"] == "200"


@responses.activate
def test_astronomy_moon(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/astronomy/moon",
        json={"code": "200", "moonrise": "17:25", "moonset": "07:42", "moonPhase": []},
        status=200,
    )
    data = astronomy_moon(client, location="101010100", date="20211120")
    assert data["code"] == "200"


def test_astronomy_moon_invalid_date(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_moon(client, location="101010100", date="2021-11-20")


def test_astronomy_moon_missing_location(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_moon(client, location="", date="20211120")


@responses.activate
def test_astronomy_moon_with_lang(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/astronomy/moon",
        json={"code": "200", "moonrise": "17:25", "moonset": "07:42", "moonPhase": []},
        status=200,
    )
    data = astronomy_moon(client, location="101010100", date="20211120", lang="en")
    assert data["code"] == "200"


@responses.activate
def test_astronomy_solar_elevation(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/astronomy/solar-elevation-angle",
        json={"code": "200", "solarElevationAngle": "42.88"},
        status=200,
    )
    data = astronomy_solar_elevation(client, location="120.34,36.08", alt=43, date="20210220", time_hm="1230", tz="0800")
    assert data["code"] == "200"


def test_astronomy_solar_elevation_invalid_time(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_solar_elevation(client, location="120.34,36.08", alt=43, date="20210220", time_hm="12:30", tz="0800")


def test_astronomy_solar_elevation_missing_location(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_solar_elevation(client, location="", alt=43, date="20210220", time_hm="1230", tz="0800")


def test_astronomy_solar_elevation_invalid_date(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        astronomy_solar_elevation(client, location="120.34,36.08", alt=43, date="2021-02-20", time_hm="1230", tz="0800")
