from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def astronomy_sun(client: QWeatherClient, *, location: str, date: str, lang: str | None = None) -> Dict[str, Any]:
    """日出日落

    功能：获取指定位置某日的日出日落时间。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度
        date: yyyyMMdd
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `sunrise`、`sunset`
    """

    if not location:
        raise ValueError("location 为必填参数")
    if not date or len(date) != 8:
        raise ValueError("date 必须为 yyyyMMdd 格式")
    params: Dict[str, Any] = {"location": location, "date": date}
    if lang:
        params["lang"] = lang
    return client.get("/v7/astronomy/sun", params=params)

