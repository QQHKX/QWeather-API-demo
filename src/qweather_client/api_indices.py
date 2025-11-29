from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from .client import QWeatherClient


def indices(client: QWeatherClient, *, location: str, type_ids: Iterable[int] | str, days: str = "1d", lang: Optional[str] = None) -> Dict[str, Any]:
    """天气指数（生活指数）

    功能：获取指定位置的生活指数数据。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度
        type_ids: 指数类型 ID 列表或逗号字符串
        days: 取值 {1d,3d}
        lang: 语言（可选）

    返回：
        JSON 字典，包含 `daily` 列表
    """

    if not location:
        raise ValueError("location 为必填参数")
    if days not in {"1d", "3d"}:
        raise ValueError("days 仅支持 1d/3d")
    if isinstance(type_ids, str):
        type_str = type_ids
    else:
        type_str = ",".join(str(i) for i in type_ids)
    if not type_str:
        raise ValueError("type_ids 不能为空")
    params: Dict[str, Any] = {"location": location, "type": type_str}
    if lang:
        params["lang"] = lang
    return client.get(f"/v7/indices/{days}", params=params)

