from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_weather_now import weather_now
from src.qweather_client.api_weather_daily import weather_daily
from src.qweather_client.api_weather_hourly import weather_hourly
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_weather_now(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "200", "now": {"temp": "24"}},
        status=200,
    )
    data = weather_now(client, location="101010100")
    assert data["now"]["temp"] == "24"


def test_weather_now_invalid_unit(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        weather_now(client, location="101010100", unit="x")


@responses.activate
def test_weather_daily(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/3d",
        json={"code": "200", "daily": []},
        status=200,
    )
    data = weather_daily(client, location="101010100", days="3d")
    assert data["code"] == "200"


def test_weather_daily_invalid_days(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        weather_daily(client, location="101010100", days="2d")


@responses.activate
def test_weather_hourly(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/24h",
        json={"code": "200", "hourly": []},
        status=200,
    )
    data = weather_hourly(client, location="101010100", hours="24h")
    assert data["code"] == "200"


def test_weather_hourly_invalid_hours(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        weather_hourly(client, location="101010100", hours="12h")

