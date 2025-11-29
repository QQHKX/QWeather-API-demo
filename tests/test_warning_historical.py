from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_warning import warning_now
from src.qweather_client.api_historical_weather import historical_weather
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_warning_now(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/warning/now",
        json={"code": "200", "warning": []},
        status=200,
    )
    data = warning_now(client, location="101020100")
    assert data["code"] == "200"


def test_historical_weather_invalid_date(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        historical_weather(client, location="101010100", date="2020-07-25")


@responses.activate
def test_historical_weather(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/historical/weather",
        json={"code": "200", "weatherDaily": {}, "weatherHourly": []},
        status=200,
    )
    data = historical_weather(client, location="101010100", date="20200725")
    assert data["code"] == "200"

