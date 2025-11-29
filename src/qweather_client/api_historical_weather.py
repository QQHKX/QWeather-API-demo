from __future__ import annotations

import re
from typing import Any, Dict

from .client import QWeatherClient


def historical_weather(client: QWeatherClient, *, location: str, date: str) -> Dict[str, Any]:
    """时间机器（近10天历史天气）

    功能：获取指定位置某日的历史天气数据（近 10 天）。

    参数：
        client: QWeatherClient 客户端
        location: 仅支持 LocationID
        date: 日期字符串 yyyyMMdd（近 10 天）

    返回：
        JSON 字典，包含 `weatherDaily` 与 `weatherHourly`
    """

    if not location:
        raise ValueError("location 为必填参数（LocationID）")
    if not re.fullmatch(r"\d{8}", date):
        raise ValueError("date 必须为 yyyyMMdd 格式")
    params = {"location": location, "date": date}
    return client.get("/v7/historical/weather", params=params)

