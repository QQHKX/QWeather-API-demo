from __future__ import annotations

import json
from _common import init_client
from src.qweather_client.api_indices import indices
from src.qweather_client.client import QWeatherAPIError


def run() -> None:
    """演示：生活指数 Indices"""

    client = init_client()
    try:
        data = indices(client, location="101010100", type_ids=[1, 2], days="1d")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except QWeatherAPIError as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    run()

