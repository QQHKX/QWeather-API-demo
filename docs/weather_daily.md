# 逐日预报（3–30天）

- 路径：`/v7/weather/{days}`，`days` 取值 `3d/7d/10d/15d/30d`
- 必填：`location`

示例：

```python
from src.qweather_client.api_weather_daily import weather_daily
weather_daily(client, location="101010100", days="3d")
```

返回值：`daily` 列表。

