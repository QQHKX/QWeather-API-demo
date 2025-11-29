# 太阳高度角与方位角

- 路径：`/v7/astronomy/solar-elevation-angle`
- 必填：`location`、`date`、`time`、`tz`、`alt`

示例：

```python
from src.qweather_client.api_astronomy_solar_elevation import astronomy_solar_elevation
astronomy_solar_elevation(client, location="120.34,36.08", alt=43, date="20210220", time_hm="1230", tz="0800")
```

返回值：`solarElevationAngle`、`solarAzimuthAngle` 等。

