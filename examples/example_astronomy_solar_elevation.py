from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_astronomy_solar_elevation import astronomy_solar_elevation
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：太阳高度角"""

    client = init_client()
    try:
        data = astronomy_solar_elevation(
            client,
            location="120.34,36.08",
            alt=43,
            date="20210220",
            time_hm="1230",
            tz="0800",
        )
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

