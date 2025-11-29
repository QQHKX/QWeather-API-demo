from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_geo_city_lookup import city_lookup
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：城市查询 City Lookup"""

    client = init_client()
    try:
        data = city_lookup(client, location="beij")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

