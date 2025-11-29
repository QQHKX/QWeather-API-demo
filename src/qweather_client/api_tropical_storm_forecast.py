from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def tropical_storm_forecast(client: QWeatherClient, *, stormid: str) -> Dict[str, Any]:
    """台风预报（指定台风）

    功能：获取指定台风的未来预报数据。

    参数：
        client: QWeatherClient 客户端
        stormid: 台风 ID（如 NP_2106）

    返回：
        JSON 字典，包含 `forecast` 列表
    """

    if not stormid:
        raise ValueError("stormid 为必填参数")
    return client.get("/v7/tropical/storm-forecast", params={"stormid": stormid})

