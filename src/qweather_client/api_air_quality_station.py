from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def air_quality_station(client: QWeatherClient, *, location_id: str, lang: str | None = None) -> Dict[str, Any]:
    """监测站空气质量（按站点ID）

    功能：获取指定监测站的污染物数据。

    参数：
        client: QWeatherClient 客户端
        location_id: 监测站点 ID（LocationID）
        lang: 语言（可选）

    返回：
        JSON 字典
    """

    if not location_id:
        raise ValueError("location_id 为必填参数")
    path = f"/airquality/v1/station/{location_id}"
    params: Dict[str, Any] = {}
    if lang:
        params["lang"] = lang
    return client.get(path, params=params)

