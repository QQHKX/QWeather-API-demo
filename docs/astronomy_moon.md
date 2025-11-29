# 月升月落与月相

- 路径：`/v7/astronomy/moon`
- 必填：`location`、`date`

示例：

```python
from src.qweather_client.api_astronomy_moon import astronomy_moon
astronomy_moon(client, location="101010100", date="20211120")
```

返回值：`moonrise`、`moonset`、`moonPhase`。

