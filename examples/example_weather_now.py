from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_weather_now import weather_now
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：天气实况 Weather Now"""

    client = init_client()
    try:
        data = weather_now(client, location="101010100")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

