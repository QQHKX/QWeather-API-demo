from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_astronomy_moon import astronomy_moon
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：月升月落与月相"""

    client = init_client()
    try:
        data = astronomy_moon(client, location="101010100", date="20211120")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

