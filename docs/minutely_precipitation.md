# 分钟级降水（中国）

- 路径：`/v7/minutely/5m`
- 必填：`location`（经纬度）

示例：

```python
from src.qweather_client.api_minutely_precipitation import minutely_precipitation
minutely_precipitation(client, location="116.38,39.91")
```

返回值：`minutely` 列表。

