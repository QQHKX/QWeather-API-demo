from __future__ import annotations

from typing import Any, Dict, Optional

from .client import QWeatherClient


def minutely_precipitation(client: QWeatherClient, *, location: str, lang: Optional[str] = None) -> Dict[str, Any]:
    """分钟级降水（中国）

    功能：获取指定经纬度未来 2 小时的分钟级降水。

    参数：
        client: QWeatherClient 客户端
        location: 经纬度字符串，如 "116.38,39.91"
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `minutely` 列表
    """

    if not location:
        raise ValueError("location 为必填参数（经纬度）")
    params: Dict[str, Any] = {"location": location}
    if lang:
        params["lang"] = lang
    return client.get("/v7/minutely/5m", params=params)

