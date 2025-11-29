from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def tropical_storm_list(client: QWeatherClient, *, basin: str, year: int) -> Dict[str, Any]:
    """台风列表（近两年）

    功能：获取指定洋盆与年份的台风列表。

    参数：
        client: QWeatherClient 客户端
        basin: 洋盆代码（如 NP）
        year: 年份

    返回：
        JSON 字典，包含 `storm` 列表
    """

    if not basin:
        raise ValueError("basin 为必填参数")
    return client.get("/v7/tropical/storm-list", params={"basin": basin, "year": year})

