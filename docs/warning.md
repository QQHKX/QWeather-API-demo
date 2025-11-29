# 灾害预警（旧版）

- 路径：`/v7/warning/now`（官方已废弃，保留示例）

示例：

```python
from src.qweather_client.api_warning import warning_now
warning_now(client, location="101020100")
```

返回值：`warning` 列表。

