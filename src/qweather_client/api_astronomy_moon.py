from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def astronomy_moon(client: QWeatherClient, *, location: str, date: str, lang: str | None = None) -> Dict[str, Any]:
    """月升月落与月相

    功能：获取指定位置某日的月升月落与月相数据。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度
        date: yyyyMMdd
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `moonrise`、`moonset`、`moonPhase`
    """

    if not location:
        raise ValueError("location 为必填参数")
    if not date or len(date) != 8:
        raise ValueError("date 必须为 yyyyMMdd 格式")
    params: Dict[str, Any] = {"location": location, "date": date}
    if lang:
        params["lang"] = lang
    return client.get("/v7/astronomy/moon", params=params)

