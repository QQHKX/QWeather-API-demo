from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_minutely_precipitation import minutely_precipitation
from src.qweather_client.api_indices import indices
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_minutely_precipitation(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/minutely/5m",
        json={"code": "200", "minutely": []},
        status=200,
    )
    data = minutely_precipitation(client, location="116.38,39.91")
    assert data["code"] == "200"


def test_minutely_precipitation_no_location(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        minutely_precipitation(client, location="")


@responses.activate
def test_indices(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/indices/1d",
        json={"code": "200", "daily": []},
        status=200,
    )
    data = indices(client, location="101010100", type_ids=[1, 2], days="1d")
    assert data["code"] == "200"


def test_indices_invalid_days(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        indices(client, location="101010100", type_ids=[1], days="2d")


def test_indices_empty_types(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        indices(client, location="101010100", type_ids=[])

