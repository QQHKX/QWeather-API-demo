from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def air_quality_current(client: QWeatherClient, *, latitude: float, longitude: float, lang: str | None = None) -> Dict[str, Any]:
    """当前空气质量（按经纬度）

    功能：获取指定经纬度的当前空气质量指数与污染物浓度。

    参数：
        client: QWeatherClient 客户端
        latitude: 纬度（最多保留 2 位小数）
        longitude: 经度（最多保留 2 位小数）
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `indexes` 与 `pollutants`
    """

    # 参数校验与格式化到 2 位小数
    lat_str = f"{latitude:.2f}"
    lon_str = f"{longitude:.2f}"
    path = f"/airquality/v1/current/{lat_str}/{lon_str}"
    params: Dict[str, Any] = {}
    if lang:
        params["lang"] = lang
    return client.get(path, params=params)

