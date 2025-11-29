from __future__ import annotations

import os
from typing import Optional
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv

from src.qweather_client import QWeatherClient


def init_client() -> QWeatherClient:
    """初始化 QWeather 客户端（从 .env 读取配置）

    读取环境变量：
    - API_HOST（必填）
    - API_KEY（任选其一）
    - JWT_TOKEN（任选其一）
    优先使用 JWT 认证，否则使用 API KEY。
    """

    load_dotenv()
    api_host = os.getenv("API_HOST", "")
    api_key: Optional[str] = os.getenv("API_KEY")
    jwt_token: Optional[str] = os.getenv("JWT_TOKEN")
    if not api_host:
        raise RuntimeError("请在 .env 中设置 API_HOST")
    return QWeatherClient(api_host=api_host, api_key=api_key, jwt_token=jwt_token)
