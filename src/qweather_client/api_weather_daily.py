from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def weather_daily(client: QWeatherClient, *, location: str, days: str) -> Dict[str, Any]:
    """逐日天气预报（3–30天）

    功能：获取指定位置的多日天气预报。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度
        days: 取值 {3d,7d,10d,15d,30d}

    返回：
        JSON 字典，包含 `daily` 列表
    """

    if not location:
        raise ValueError("location 为必填参数")
    if days not in {"3d", "7d", "10d", "15d", "30d"}:
        raise ValueError("days 仅支持 3d/7d/10d/15d/30d")
    return client.get(f"/v7/weather/{days}", params={"location": location})

