from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple

import requests


class QWeatherAPIError(Exception):
    """通用 API 异常，包含和风天气返回的错误代码与信息。"""

    def __init__(self, code: str, message: str, *, http_status: int | None = None) -> None:
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(f"QWeather API Error code={code} http={http_status} message={message}")


class QWeatherAuthError(QWeatherAPIError):
    """认证异常，通常对应 401 或鉴权失败场景。"""


class QWeatherRateLimitError(QWeatherAPIError):
    """频率限制异常，通常对应 429。"""


@dataclass
class ClientConfig:
    """客户端配置数据类。

    Attributes:
        api_host: 服务端 Host，例如 `api.qweather.com`
        api_key: 使用 API KEY 鉴权时的密钥
        jwt_token: 使用 JWT 鉴权时的令牌（`Authorization: Bearer`）
        timeout: 请求超时时间（秒）
        user_agent: 自定义 UA 标识
    """

    api_host: str
    api_key: Optional[str] = None
    jwt_token: Optional[str] = None
    timeout: int = 15
    user_agent: str = "qweather-client/1.0"


class QWeatherClient:
    """和风天气统一客户端，负责认证、发送请求与通用错误处理。

    示例：
        >>> client = QWeatherClient(api_host="api.qweather.com", api_key="YOUR_KEY")
        >>> data = client.get("/v7/weather/now", params={"location": "101010100"})
        >>> print(data["now"]["temp"])  # 访问解析后的 JSON
    """

    def __init__(self, *, api_host: str, api_key: str | None = None, jwt_token: str | None = None, timeout: int = 15, user_agent: str | None = None) -> None:
        # 构造函数：初始化基础配置与会话
        if not api_host:
            raise ValueError("api_host 不能为空")
        self.config = ClientConfig(
            api_host=api_host,
            api_key=api_key,
            jwt_token=jwt_token,
            timeout=timeout,
            user_agent=user_agent or "qweather-client/1.0",
        )
        self._session = requests.Session()

    def _build_headers(self, extra: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
        # 组装请求头：根据 API KEY 或 JWT 选择认证方式
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": self.config.user_agent,
        }
        if self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"
        elif self.config.api_key:
            headers["X-QW-Api-Key"] = self.config.api_key
        if extra:
            headers.update(dict(extra))
        return headers

    def _request(self, method: str, path: str, *, params: Optional[Mapping[str, Any]] = None, headers: Optional[Mapping[str, str]] = None) -> Dict[str, Any]:
        # 发送 HTTP 请求并统一解析响应与错误
        if not path.startswith("/"):
            raise ValueError("path 必须以 '/' 开头")
        url = f"https://{self.config.api_host}{path}"
        response = self._session.request(
            method=method.upper(),
            url=url,
            params=params,
            headers=self._build_headers(headers),
            timeout=self.config.timeout,
        )
        http_status = response.status_code
        text = response.text
        try:
            data = response.json()
        except json.JSONDecodeError:
            # 无 JSON 响应体的 404 等错误
            if http_status == 404:
                raise QWeatherAPIError("404", "路径或路径参数错误", http_status=http_status)
            raise QWeatherAPIError(str(http_status), f"非 JSON 响应: {text[:200]}", http_status=http_status)

        # 检查业务码（QWeather 约定在 JSON 中返回 code 字段）
        code = str(data.get("code", "200"))
        if http_status >= 400 or code != "200":
            message = self._summarize_error(code, data)
            if code == "401" or http_status == 401:
                raise QWeatherAuthError(code, message, http_status=http_status)
            if code == "429" or http_status == 429:
                raise QWeatherRateLimitError(code, message, http_status=http_status)
            raise QWeatherAPIError(code, message, http_status=http_status)
        return data

    @staticmethod
    def _summarize_error(code: str, data: Mapping[str, Any]) -> str:
        # 汇总错误信息：结合官方错误码分类返回易读文本
        mapping = {
            "400": "参数非法/缺失/位置不存在/数据暂不可用",
            "401": "认证失败（检查 KEY 或 JWT）",
            "403": "无权限或安全限制（额度/账单/Host/账号暂停）",
            "404": "路径或路径参数错误",
            "429": "请求过多或额度超限（请指数退避）",
        }
        base = mapping.get(code, "未知错误")
        extra = data.get("message") or data.get("reason") or ""
        return f"{base}{'：' + str(extra) if extra else ''}"

    # 对外方法
    def get(self, path: str, *, params: Optional[Mapping[str, Any]] = None, headers: Optional[Mapping[str, str]] = None) -> Dict[str, Any]:
        # GET 请求封装
        return self._request("GET", path, params=params, headers=headers)

    def close(self) -> None:
        # 关闭底层会话
        self._session.close()

