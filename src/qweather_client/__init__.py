"""qweather_client 包初始化

此包包含和风天气 API 的统一客户端与各功能模块。
"""

from .client import QWeatherClient, QWeatherAPIError, QWeatherAuthError, QWeatherRateLimitError

__all__ = [
    "QWeatherClient",
    "QWeatherAPIError",
    "QWeatherAuthError",
    "QWeatherRateLimitError",
]

