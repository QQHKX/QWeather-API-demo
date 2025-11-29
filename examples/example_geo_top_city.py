from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_geo_top_city import top_city
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：热门城市 Top City"""

    client = init_client()
    try:
        data = top_city(client, number=5, range="cn")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

