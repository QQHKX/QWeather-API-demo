from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def warning_now(client: QWeatherClient, *, location: str) -> Dict[str, Any]:
    """灾害预警（旧版接口示例）

    功能：获取指定位置的当前预警信息（旧版 /v7/warning/now）。

    参数：
        client: QWeatherClient 客户端
        location: LocationID 或经纬度

    返回：
        JSON 字典，包含 `warning` 列表
    """

    if not location:
        raise ValueError("location 为必填参数")
    return client.get("/v7/warning/now", params={"location": location})

