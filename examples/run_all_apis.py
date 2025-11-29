from __future__ import annotations

import json
import time
from typing import Any, Callable, Dict, List, Tuple
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from colorama import init as color_init, Fore, Style
    color_init(autoreset=True)
except Exception:
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        CYAN = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""

from src.qweather_client.client import QWeatherAPIError
from examples._common import init_client

from src.qweather_client.api_geo_city_lookup import city_lookup
from src.qweather_client.api_geo_top_city import top_city
from src.qweather_client.api_weather_now import weather_now
from src.qweather_client.api_weather_daily import weather_daily
from src.qweather_client.api_weather_hourly import weather_hourly
from src.qweather_client.api_minutely_precipitation import minutely_precipitation
from src.qweather_client.api_indices import indices
from src.qweather_client.api_air_quality_current import air_quality_current
from src.qweather_client.api_air_quality_station import air_quality_station
from src.qweather_client.api_warning import warning_now
from src.qweather_client.api_historical_weather import historical_weather
from src.qweather_client.api_astronomy_sun import astronomy_sun
from src.qweather_client.api_astronomy_moon import astronomy_moon
from src.qweather_client.api_astronomy_solar_elevation import astronomy_solar_elevation
from src.qweather_client.api_tropical_storm_list import tropical_storm_list
from src.qweather_client.api_tropical_storm_track import tropical_storm_track
from src.qweather_client.api_tropical_storm_forecast import tropical_storm_forecast


@dataclass
class TestSpec:
    """测试用例规格

    字段：
        name: 用例名称
        request_desc: 请求语义化描述
        run: 实际调用函数
        summarize: 根据返回数据输出语义化摘要
    """

    name: str
    request_desc: str
    run: Callable[[], Dict[str, Any]]
    summarize: Callable[[Dict[str, Any]], str]


def run_all() -> None:
    """一键测试所有 API 功能（语义化输出 + 统计）

    行为：
        - 初始化客户端
        - 构造每个 API 的测试规格（请求描述 + 结果摘要）
        - 执行并输出彩色状态、语义化信息与局部 JSON 片段
        - 汇总统计信息（成功/失败/耗时）
    """

    try:
        client = init_client()
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}初始化客户端失败：{e}{Style.RESET_ALL}")
        print("请在项目根目录的 .env 中设置 API_HOST 与 API_KEY 或 JWT_TOKEN")
        return

    today = datetime.now().strftime("%Y%m%d")
    recent = (datetime.now() - timedelta(days=3)).strftime("%Y%m%d")

    active_storm_id: str | None = None
    try:
        storm_list = tropical_storm_list(client, basin="NP", year=int(datetime.now().strftime("%Y")))
        for s in storm_list.get("storm", []):
            if s.get("isActive") == "1":
                active_storm_id = s.get("id")
                break
        if not active_storm_id and storm_list.get("storm"):
            active_storm_id = storm_list["storm"][0].get("id")
    except Exception:
        active_storm_id = None

    specs: List[TestSpec] = [
        TestSpec(
            name="Geo: City Lookup",
            request_desc="按关键字查询城市（location=beij）",
            run=lambda: city_lookup(client, location="beij"),
            summarize=lambda d: f"匹配 {len(d.get('location', []))} 条，首项：{(d.get('location') or [{}])[0].get('name', '-')}",
        ),
        TestSpec(
            name="Geo: Top City",
            request_desc="热门城市列表（range=cn, number=5）",
            run=lambda: top_city(client, number=5, range="cn"),
            summarize=lambda d: f"返回条数：{len(d.get('topCityList') or d.get('location') or [])}",
        ),
        TestSpec(
            name="Weather: Now",
            request_desc="天气实况（location=101010100）",
            run=lambda: weather_now(client, location="101010100"),
            summarize=lambda d: f"温度：{d.get('now', {}).get('temp', '-')}，天气：{d.get('now', {}).get('text', '-')}",
        ),
        TestSpec(
            name="Weather: Daily",
            request_desc="3日预报（location=101010100, days=3d）",
            run=lambda: weather_daily(client, location="101010100", days="3d"),
            summarize=lambda d: f"天数：{len(d.get('daily', []))}，首日范围：{(d.get('daily') or [{}])[0].get('tempMin', '-')}-{(d.get('daily') or [{}])[0].get('tempMax', '-')}",
        ),
        TestSpec(
            name="Weather: Hourly",
            request_desc="24小时预报（location=101010100, hours=24h）",
            run=lambda: weather_hourly(client, location="101010100", hours="24h"),
            summarize=lambda d: f"小时数：{len(d.get('hourly', []))}，首小时温度：{(d.get('hourly') or [{}])[0].get('temp', '-')}",
        ),
        TestSpec(
            name="Minutely: 5m",
            request_desc="分钟级降水（location=116.38,39.91）",
            run=lambda: minutely_precipitation(client, location="116.38,39.91"),
            summarize=lambda d: f"摘要：{d.get('summary', '-')}",
        ),
        TestSpec(
            name="Indices",
            request_desc="生活指数（location=101010100, type=1,2, days=1d）",
            run=lambda: indices(client, location="101010100", type_ids=[1, 2], days="1d"),
            summarize=lambda d: f"指数条数：{len(d.get('daily', []))}",
        ),
        TestSpec(
            name="Air: Current",
            request_desc="空气质量（经纬度=39.90,116.40）",
            run=lambda: air_quality_current(client, latitude=39.90, longitude=116.40),
            summarize=lambda d: f"主指数：{(d.get('indexes') or [{}])[0].get('name', '-')}/{(d.get('indexes') or [{}])[0].get('aqi', '-')}",
        ),
        TestSpec(
            name="Air: Station",
            request_desc="空气质量（站点=P53763）",
            run=lambda: air_quality_station(client, location_id="P53763"),
            summarize=lambda d: f"污染物数：{len(d.get('pollutants', []))}",
        ),
        TestSpec(
            name="Warning (legacy)",
            request_desc="旧版灾害预警（location=101020100）",
            run=lambda: warning_now(client, location="101020100"),
            summarize=lambda d: f"预警条数：{len(d.get('warning', []))}",
        ),
        TestSpec(
            name="Historical",
            request_desc=f"历史天气（location=101010100, date={recent}）",
            run=lambda: historical_weather(client, location="101010100", date=recent),
            summarize=lambda d: f"最高/最低：{d.get('weatherDaily', {}).get('tempMax', '-')}/{d.get('weatherDaily', {}).get('tempMin', '-')}",
        ),
        TestSpec(
            name="Astronomy: Sun",
            request_desc=f"日出日落（location=101010100, date={today}）",
            run=lambda: astronomy_sun(client, location="101010100", date=today),
            summarize=lambda d: f"日出/日落：{d.get('sunrise', '-')}/{d.get('sunset', '-')}",
        ),
        TestSpec(
            name="Astronomy: Moon",
            request_desc=f"月升月落与月相（location=101010100, date={today}）",
            run=lambda: astronomy_moon(client, location="101010100", date=today),
            summarize=lambda d: f"月升/月落：{d.get('moonrise', '-')}/{d.get('moonset', '-')}; 月相：{((d.get('moonPhase') or [{}])[0]).get('name', '-')}",
        ),
        TestSpec(
            name="Astronomy: Solar Elevation",
            request_desc=f"太阳高度角（location=120.34,36.08, date={today}, time=1230, tz=0800, alt=43）",
            run=lambda: astronomy_solar_elevation(client, location="120.34,36.08", alt=43, date=today, time_hm="1230", tz="0800"),
            summarize=lambda d: f"高度/方位角：{d.get('solarElevationAngle', '-')}/{d.get('solarAzimuthAngle', '-')}",
        ),
        TestSpec(
            name="Tropical: Storm List",
            request_desc=f"台风列表（basin=NP, year={datetime.now().strftime('%Y')}）",
            run=lambda: tropical_storm_list(client, basin="NP", year=int(datetime.now().strftime("%Y"))),
            summarize=lambda d: f"台风数量：{len(d.get('storm', []))}；活动数：{sum(1 for s in (d.get('storm') or []) if s.get('isActive')=='1')}",
        ),
        TestSpec(
            name="Tropical: Storm Track",
            request_desc=f"台风路径（stormid={active_storm_id or 'NP_2021'}）",
            run=lambda: tropical_storm_track(client, stormid=active_storm_id or "NP_2021"),
            summarize=lambda d: f"路径点数：{len(d.get('track', []))}",
        ),
        TestSpec(
            name="Tropical: Storm Forecast",
            request_desc=f"台风预报（stormid={active_storm_id or 'NP_2106'}）",
            run=lambda: tropical_storm_forecast(client, stormid=active_storm_id or "NP_2106"),
            summarize=lambda d: f"预报点数：{len(d.get('forecast', []))}",
        ),
    ]

    results: List[Tuple[str, str, float]] = []
    total = len(specs)
    success = 0
    failed = 0

    for spec in specs:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}==== {spec.name} ===={Style.RESET_ALL}")
        print(f"{Fore.CYAN}请求：{spec.request_desc}{Style.RESET_ALL}")
        t0 = time.time()
        try:
            data = spec.run()
            summary = spec.summarize(data)
            print(f"{Fore.GREEN}返回：{summary}{Style.RESET_ALL}")
            snippet = json.dumps({k: data.get(k) for k in list(data.keys())[:2]}, ensure_ascii=False, indent=2)
            print(snippet)
            status = "成功"
            success += 1
        except QWeatherAPIError as e:
            print(f"{Fore.RED}API 错误：{e}{Style.RESET_ALL}")
            status = "失败"
            failed += 1
        except Exception as e:
            print(f"{Fore.RED}运行异常：{e}{Style.RESET_ALL}")
            status = "失败"
            failed += 1
        dt = time.time() - t0
        results.append((spec.name, status, dt))
        time.sleep(0.2)

    print(f"\n{Style.BRIGHT}====== 测试统计 ======{Style.RESET_ALL}")
    for name, status, dt in results:
        color = Fore.GREEN if status == "成功" else Fore.RED
        print(f"{color}{name}：{status}（{dt:.2f}s）{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}总计：{total}；成功：{success}；失败：{failed}；成功率：{(success/total*100):.2f}%{Style.RESET_ALL}")


if __name__ == "__main__":
    run_all()
