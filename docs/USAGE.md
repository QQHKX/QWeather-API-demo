# 使用说明

## 客户端初始化

```python
from src.qweather_client import QWeatherClient
client = QWeatherClient(api_host="你的主机名", api_key="你的密钥")
```

若提供 `jwt_token` 则优先使用 JWT 鉴权：

```python
client = QWeatherClient(api_host="你的主机名", jwt_token="你的JWT")
```

## 通用错误处理

- 返回 JSON 内 `code != "200"` 或 HTTP 状态码异常将抛出 `QWeatherAPIError`
- `401` 抛出 `QWeatherAuthError`
- `429` 抛出 `QWeatherRateLimitError`

在示例脚本中均已演示 try/except 的用法。

## 参数与返回

每个 API 的参数校验与返回字段见对应文档文件。

