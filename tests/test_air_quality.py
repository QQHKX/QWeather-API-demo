from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_air_quality_current import air_quality_current
from src.qweather_client.api_air_quality_station import air_quality_station
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_air_quality_current(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/airquality/v1/current/39.90/116.40",
        json={"code": "200", "indexes": []},
        status=200,
    )
    data = air_quality_current(client, latitude=39.904, longitude=116.404)
    assert data["code"] == "200"


@responses.activate
def test_air_quality_station(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/airquality/v1/station/P53763",
        json={"code": "200", "pollutants": []},
        status=200,
    )
    data = air_quality_station(client, location_id="P53763")
    assert data["code"] == "200"


def test_air_quality_station_missing_id(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        air_quality_station(client, location_id="")


@responses.activate
def test_air_quality_current_with_lang(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/airquality/v1/current/39.90/116.40",
        json={"code": "200", "indexes": []},
        status=200,
    )
    data = air_quality_current(client, latitude=39.90, longitude=116.40, lang="en")
    assert data["code"] == "200"


@responses.activate
def test_air_quality_station_with_lang(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/airquality/v1/station/P53763",
        json={"code": "200", "pollutants": []},
        status=200,
    )
    data = air_quality_station(client, location_id="P53763", lang="en")
    assert data["code"] == "200"
