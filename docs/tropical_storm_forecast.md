# 台风预报

- 路径：`/v7/tropical/storm-forecast`
- 必填：`stormid`

示例：

```python
from src.qweather_client.api_tropical_storm_forecast import tropical_storm_forecast
tropical_storm_forecast(client, stormid="NP_2106")
```

返回值：`forecast` 列表。

