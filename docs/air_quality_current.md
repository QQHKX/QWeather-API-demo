# 空气质量（当前，经纬度）

- 路径：`/airquality/v1/current/{latitude}/{longitude}`
- 路径参数：`latitude`、`longitude`（最多 2 位小数）

示例：

```python
from src.qweather_client.api_air_quality_current import air_quality_current
air_quality_current(client, latitude=39.90, longitude=116.40)
```

返回值：`indexes`、`pollutants`。

