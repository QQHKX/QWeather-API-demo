from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_tropical_storm_list import tropical_storm_list
from src.qweather_client.api_tropical_storm_track import tropical_storm_track
from src.qweather_client.api_tropical_storm_forecast import tropical_storm_forecast
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_tropical_storm_list(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/tropical/storm-list",
        json={"code": "200", "storm": []},
        status=200,
    )
    data = tropical_storm_list(client, basin="NP", year=2024)
    assert data["code"] == "200"


def test_tropical_storm_list_missing_basin(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        tropical_storm_list(client, basin="", year=2024)


@responses.activate
def test_tropical_storm_track(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/tropical/storm-track",
        json={"code": "200", "track": []},
        status=200,
    )
    data = tropical_storm_track(client, stormid="NP_2021")
    assert data["code"] == "200"


@responses.activate
def test_tropical_storm_forecast(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/tropical/storm-forecast",
        json={"code": "200", "forecast": []},
        status=200,
    )
    data = tropical_storm_forecast(client, stormid="NP_2106")
    assert data["code"] == "200"

