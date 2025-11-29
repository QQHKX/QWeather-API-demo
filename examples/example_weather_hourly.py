from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_weather_hourly import weather_hourly
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：逐小时预报 Weather Hourly"""

    client = init_client()
    try:
        data = weather_hourly(client, location="101010100", hours="24h")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

