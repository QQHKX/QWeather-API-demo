from __future__ import annotations

import pytest

from src.qweather_client import QWeatherClient


@pytest.fixture()
def client() -> QWeatherClient:
    """测试用客户端：使用虚拟主机与 API KEY"""

    return QWeatherClient(api_host="example.com", api_key="test-key")

