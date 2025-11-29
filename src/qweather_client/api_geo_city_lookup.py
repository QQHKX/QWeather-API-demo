from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from .client import QWeatherClient


def city_lookup(client: QWeatherClient, *, location: str, adm: Optional[str] = None, range: Optional[str] = None, number: Optional[int] = None, lang: Optional[str] = None) -> Dict[str, Any]:
    """城市查询（City Lookup）

    功能：根据文本、LocationID、经纬度或中国 Adcode 查询城市信息。

    参数：
        client: QWeatherClient 客户端
        location: 查询关键字或坐标，如 "beij"、"101010100" 或 "116.38,39.91"
        adm: 上级行政区过滤（可选）
        range: 国家代码（ISO 3166-1，可选）
        number: 返回数量 1–20（可选，默认 10）
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `location` 列表等信息

    示例：
        >>> city_lookup(client, location="beij")
    """

    # 参数校验：location 必填，number 范围限制
    if not location:
        raise ValueError("location 为必填参数")
    if number is not None and not (1 <= number <= 20):
        raise ValueError("number 必须在 1–20 范围内")

    params: Dict[str, Any] = {"location": location}
    if adm:
        params["adm"] = adm
    if range:
        params["range"] = range
    if number:
        params["number"] = number
    if lang:
        params["lang"] = lang

    # 调用客户端发送 GET 请求
    return client.get("/geo/v2/city/lookup", params=params)

