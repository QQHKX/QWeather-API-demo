# 台风路径

- 路径：`/v7/tropical/storm-track`
- 必填：`stormid`

示例：

```python
from src.qweather_client.api_tropical_storm_track import tropical_storm_track
tropical_storm_track(client, stormid="NP_2021")
```

返回值：路径点列表。

