# 热门城市（Top City）

- 路径：`/geo/v2/city/top`
- 可选参数：`range`、`number`、`lang`

示例代码：

```python
from src.qweather_client.api_geo_top_city import top_city
top_city(client, number=5, range="cn")
```

返回值：热门城市列表。

