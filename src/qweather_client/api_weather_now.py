from __future__ import annotations

from typing import Any, Dict, Optional

from .client import QWeatherClient


def weather_now(client: QWeatherClient, *, location: str, lang: Optional[str] = None, unit: Optional[str] = None) -> Dict[str, Any]:
    """天气实况（Weather Now）

    功能：获取指定位置的当前天气实况。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度 "lon,lat"
        lang: 语言（可选）
        unit: 单位（m/i，可选）

    返回：
        JSON 字典，包含 `now` 节点
    """

    if not location:
        raise ValueError("location 为必填参数")
    if unit is not None and unit not in {"m", "i"}:
        raise ValueError("unit 仅支持 'm' 或 'i'")

    params: Dict[str, Any] = {"location": location}
    if lang:
        params["lang"] = lang
    if unit:
        params["unit"] = unit
    return client.get("/v7/weather/now", params=params)

