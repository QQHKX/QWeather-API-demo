# 空气质量（监测站）

- 路径：`/airquality/v1/station/{LocationID}`
- 路径参数：`LocationID`

示例：

```python
from src.qweather_client.api_air_quality_station import air_quality_station
air_quality_station(client, location_id="P53763")
```

返回值：污染物数据列表。

