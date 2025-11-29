from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_historical_weather import historical_weather
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：时间机器（历史天气）"""

    client = init_client()
    try:
        data = historical_weather(client, location="101010100", date="20200725")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

