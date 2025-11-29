# 日出日落

- 路径：`/v7/astronomy/sun`
- 必填：`location`、`date`

示例：

```python
from src.qweather_client.api_astronomy_sun import astronomy_sun
astronomy_sun(client, location="101010100", date="20210220")
```

返回值：`sunrise`、`sunset`。

