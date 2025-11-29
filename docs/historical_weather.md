# 时间机器（历史天气）

- 路径：`/v7/historical/weather`
- 必填：`location`（LocationID）、`date=yyyyMMdd`

示例：

```python
from src.qweather_client.api_historical_weather import historical_weather
historical_weather(client, location="101010100", date="20200725")
```

返回值：`weatherDaily` 与 `weatherHourly`。

