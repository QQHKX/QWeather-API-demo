from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_warning import warning_now
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：灾害预警（旧版）"""

    client = init_client()
    try:
        data = warning_now(client, location="101020100")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

