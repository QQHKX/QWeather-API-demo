from __future__ import annotations

import json
import responses
import pytest

from src.qweather_client.client import QWeatherClient, QWeatherAPIError, QWeatherAuthError, QWeatherRateLimitError


@responses.activate
def test_auth_header_api_key(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "200", "now": {"temp": "24"}},
        status=200,
    )
    data = client.get("/v7/weather/now", params={"location": "101010100"})
    assert data["code"] == "200"


@responses.activate
def test_auth_header_jwt() -> None:
    client = QWeatherClient(api_host="example.com", jwt_token="jwt")
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "200", "now": {"temp": "24"}},
        status=200,
    )
    data = client.get("/v7/weather/now", params={"location": "101010100"})
    assert data["code"] == "200"


@responses.activate
def test_error_handling_400_code(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "400", "message": "参数错误"},
        status=200,
    )
    with pytest.raises(QWeatherAPIError):
        client.get("/v7/weather/now", params={"location": ""})


@responses.activate
def test_error_handling_401(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "401", "message": "认证失败"},
        status=401,
    )
    with pytest.raises(QWeatherAuthError):
        client.get("/v7/weather/now", params={"location": "101010100"})


@responses.activate
def test_error_handling_429(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/v7/weather/now",
        json={"code": "429", "message": "超限"},
        status=429,
    )
    with pytest.raises(QWeatherRateLimitError):
        client.get("/v7/weather/now", params={"location": "101010100"})


@responses.activate
def test_non_json_404(client: QWeatherClient) -> None:
    responses.add(
        responses.GET,
        "https://example.com/notfound",
        body="Not Found",
        status=404,
    )
    with pytest.raises(QWeatherAPIError):
        client.get("/notfound")

