from __future__ import annotations

from typing import Any, Dict

from .client import QWeatherClient


def astronomy_solar_elevation(
    client: QWeatherClient,
    *,
    location: str,
    date: str,
    time_hm: str,
    tz: str,
    alt: int,
) -> Dict[str, Any]:
    """太阳高度角与方位角

    功能：获取指定地点与时间的太阳高度角与方位角等数据。

    参数：
        client: QWeatherClient 客户端
        location: 经纬度 "lon,lat"
        date: yyyyMMdd
        time_hm: HHmm
        tz: 时区，如 0800/-0530
        alt: 海拔（米）

    返回：
        JSON 字典，包含 `solarElevationAngle`、`solarAzimuthAngle` 等字段
    """

    if not location:
        raise ValueError("location 为必填参数")
    if len(date) != 8:
        raise ValueError("date 必须为 yyyyMMdd 格式")
    if len(time_hm) != 4:
        raise ValueError("time_hm 必须为 HHmm 格式")
    params: Dict[str, Any] = {
        "location": location,
        "date": date,
        "time": time_hm,
        "tz": tz,
        "alt": alt,
    }
    return client.get("/v7/astronomy/solar-elevation-angle", params=params)

