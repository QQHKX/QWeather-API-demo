from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def weather_hourly(client: QWeatherClient, *, location: str, hours: str) -> Dict[str, Any]:
    """逐小时天气预报（24–168小时）

    功能：获取指定位置的逐小时预报。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度
        hours: 取值 {24h,72h,168h}

    返回：
        JSON 字典，包含 `hourly` 列表
    """

    if not location:
        raise ValueError("location 为必填参数")
    if hours not in {"24h", "72h", "168h"}:
        raise ValueError("hours 仅支持 24h/72h/168h")
    return client.get(f"/v7/weather/{hours}", params={"location": location})

