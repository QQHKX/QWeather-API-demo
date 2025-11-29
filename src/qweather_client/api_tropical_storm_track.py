from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def tropical_storm_track(client: QWeatherClient, *, stormid: str) -> Dict[str, Any]:
    """台风路径（活动台风）

    功能：获取指定台风的路径点信息。

    参数：
        client: QWeatherClient 客户端
        stormid: 台风 ID（如 NP_2021）

    返回：
        JSON 字典
    """

    if not stormid:
        raise ValueError("stormid 为必填参数")
    return client.get("/v7/tropical/storm-track", params={"stormid": stormid})

