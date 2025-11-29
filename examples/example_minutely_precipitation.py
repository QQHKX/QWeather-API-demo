from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_minutely_precipitation import minutely_precipitation
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：分钟级降水 Minutely"""

    client = init_client()
    try:
        data = minutely_precipitation(client, location="116.38,39.91")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

