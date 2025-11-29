# 台风列表

- 路径：`/v7/tropical/storm-list`
- 必填：`basin`、`year`

示例：

```python
from src.qweather_client.api_tropical_storm_list import tropical_storm_list
tropical_storm_list(client, basin="NP", year=2024)
```

返回值：`storm` 列表。

