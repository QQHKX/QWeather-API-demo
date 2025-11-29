from __future__ import annotations

from typing import Any, Dict, Optional

from .client import QWeatherClient


def top_city(client: QWeatherClient, *, range: Optional[str] = None, number: Optional[int] = None, lang: Optional[str] = None) -> Dict[str, Any]:
    """热门城市（Top City）

    功能：获取热门城市列表。

    参数：
        client: QWeatherClient 客户端
        range: 国家代码范围（可选）
        number: 返回数量 1–20（可选）
        lang: 语言（可选）

    返回：
        JSON 字典
    """

    if number is not None and not (1 <= number <= 20):
        raise ValueError("number 必须在 1–20 范围内")

    params: Dict[str, Any] = {}
    if range:
        params["range"] = range
    if number:
        params["number"] = number
    if lang:
        params["lang"] = lang
    return client.get("/geo/v2/city/top", params=params)

