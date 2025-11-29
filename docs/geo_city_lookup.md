# 城市查询（City Lookup）

- 路径：`/geo/v2/city/lookup`
- 必填参数：`location`
- 可选参数：`adm`、`range`、`number`、`lang`

示例代码：

```python
from src.qweather_client.api_geo_city_lookup import city_lookup
city_lookup(client, location="beij")
```

返回值：包含 `location` 列表等。

