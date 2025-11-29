# 天气实况（Weather Now）

- 路径：`/v7/weather/now`
- 必填：`location`
- 可选：`lang`、`unit=m/i`

示例：

```python
from src.qweather_client.api_weather_now import weather_now
weather_now(client, location="101010100")
```

返回值：`now` 节点。

