# 逐小时预报（24–168小时）

- 路径：`/v7/weather/{hours}`，`hours` 取值 `24h/72h/168h`
- 必填：`location`

示例：

```python
from src.qweather_client.api_weather_hourly import weather_hourly
weather_hourly(client, location="101010100", hours="24h")
```

返回值：`hourly` 列表。

