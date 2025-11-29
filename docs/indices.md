# 天气指数（生活指数）

- 路径：`/v7/indices/{days}`，`days` 取值 `1d/3d`
- 必填：`location`、`type`（多个用逗号）

示例：

```python
from src.qweather_client.api_indices import indices
indices(client, location="101010100", type_ids=[1, 2], days="1d")
```

返回值：`daily` 列表。

