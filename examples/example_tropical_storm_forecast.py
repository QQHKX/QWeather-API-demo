from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_tropical_storm_forecast import tropical_storm_forecast
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：台风预报"""

    client = init_client()
    try:
        data = tropical_storm_forecast(client, stormid="NP_2106")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

