from __future__ import annotations

import responses
import pytest

from src.qweather_client.api_geo_city_lookup import city_lookup
from src.qweather_client.api_geo_top_city import top_city
from src.qweather_client.client import QWeatherClient


@responses.activate
def test_city_lookup(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/geo/v2/city/lookup",
        json={"code": "200", "location": [{"name": "北京"}]},
        status=200,
    )
    data = city_lookup(client, location="beij")
    assert data["location"][0]["name"] == "北京"


def test_city_lookup_number_range_validation(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        city_lookup(client, location="beij", number=0)


def test_city_lookup_missing_location(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        city_lookup(client, location="")


@responses.activate
def test_city_lookup_with_optional_params(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/geo/v2/city/lookup",
        json={"code": "200", "location": []},
        status=200,
    )
    data = city_lookup(client, location="beij", adm="北京市", range="cn", number=3, lang="en")
    assert data["code"] == "200"


@responses.activate
def test_top_city(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/geo/v2/city/top",
        json={"code": "200", "topCityList": []},
        status=200,
    )
    data = top_city(client, number=5, range="cn")
    assert data["code"] == "200"


def test_top_city_invalid_number(client: QWeatherClient) -> None:
    with pytest.raises(ValueError):
        top_city(client, number=99)
