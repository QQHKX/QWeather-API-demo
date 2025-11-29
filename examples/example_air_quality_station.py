from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_air_quality_station import air_quality_station
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：空气质量（监测站）"""

    client = init_client()
    try:
        data = air_quality_station(client, location_id="P53763")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

