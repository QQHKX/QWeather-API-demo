# 和风天气 Web API 全量功能说明（Markdown版）

> 本文档覆盖 GeoAPI、天气实况/预报、分钟级降水、天气指数、空气质量（v1）、灾害预警、时间机器、天文、热带气旋等主要接口；包含接口标识、URL/方法、参数、示例响应、频率与错误码说明，并附官方参考链接以便同步更新。

- 认证方式（二选一）：
  - API KEY：在请求头传 `X-QW-Api-Key: ${API_KEY}`（推荐在服务端使用）
  - JWT：在请求头传 `Authorization: Bearer <JWT>`（EdDSA/Ed25519 签名）
- 主机名：`${API_HOST}`（从控制台获取；示例均以此占位符表示）
- 压缩：响应默认 Gzip 压缩
- 归因：在产品界面注明“天气服务由和风天气驱动”并链接 https://www.qweather.com；使用预警/空气质量数据需完整展示 `refer.sources`/`metadata.sources`
- 错误码：采用 v2 分类，详见文末“错误代码对照表”

参考：
- 构建请求与认证：https://dev.qweather.com/en/docs/configuration/api-config/ 、https://dev.qweather.com/en/docs/configuration/authentication/
- 归因要求：https://dev.qweather.com/docs/terms/attribution/ 、https://dev.qweather.com/docs/account/management/ 、https://dev.qweather.com/docs/start/

---

## GeoAPI

### 城市查询（City Lookup）
- 标识：`/geo/v2/city/lookup`
- 方法：`GET`
- 参数：
  - 必填：`location`（文本 / LocationID / 经纬度 `lon,lat` / 中国 Adcode）
  - 可选：`adm`（上级行政区过滤）、`range`（ISO 3166-1 国家代码）、`number`（1–20，默认10）、`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/geo/v2/city/lookup?location=beij"
  ```
- 返回（节选）：
  ```json
  {
    "code":"200",
    "location":[
      {"name":"北京","id":"101010100","lat":"39.90499","lon":"116.40529","adm2":"北京","adm1":"北京市","country":"中国","tz":"Asia/Shanghai","type":"city","rank":"10","fxLink":"https://www.qweather.com/weather/beijing-101010100.html"}
    ]
  }
  ```
- 参考：https://dev.qweather.com/en/docs/api/geoapi/city-lookup/

### 热门城市（Top City）
- 标识：`/geo/v2/city/top`
- 方法：`GET`
- 参数：
  - 可选：`range`、`number`、`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/geo/v2/city/top?number=5&range=cn"
  ```
- 参考：https://dev.qweather.com/en/docs/api/geoapi/top-city/

---

## 天气实况（Real-time Weather）
- 标识：`/v7/weather/now`
- 方法：`GET`
- 参数：
  - 必填：`location`（LocationID 或经纬度 `lon,lat`）
  - 可选：`lang`、`unit`（`m`/`i`）
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/weather/now?location=101010100"
  ```
- 返回（节选）：
  ```json
  {
    "code":"200",
    "updateTime":"2020-06-30T22:00+08:00",
    "fxLink":"http://hfx.link/2ax1",
    "now":{
      "obsTime":"2020-06-30T21:40+08:00","temp":"24","feelsLike":"26","icon":"101","text":"多云",
      "wind360":"123","windDir":"东南风","windSpeed":"3","humidity":"72","precip":"0.0",
      "pressure":"1003","vis":"16","cloud":"10","dew":"21"
    },
    "refer":{"sources":["QWeather","NMC","ECMWF"],"license":["QWeather Developers License"]}
  }
  ```
- 参考：https://dev.qweather.com/en/docs/api/weather/weather-now/

---

## 天气逐日预报（3–30天）
- 标识：`/v7/weather/{days}`，`days ∈ {3d,7d,10d,15d,30d}`
- 方法：`GET`
- 参数：
  - 必填：`location`
  - 可选：`lang`、`unit`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/weather/3d?location=101010100"
  ```
- 返回（节选）：
  ```json
  {
    "code":"200",
    "updateTime":"2021-11-15T16:35+08:00",
    "fxLink":"http://hfx.link/2ax1",
    "daily":[
      {"fxDate":"2021-11-15","sunrise":"06:58","sunset":"16:59","tempMax":"12","tempMin":"-1","textDay":"多云","textNight":"晴","humidity":"65","precip":"0.0","pressure":"1020","vis":"25","uvIndex":"3"}
    ]
  }
  ```
- 参考：https://dev.qweather.com/en/docs/api/weather/weather-daily-forecast/

---

## 天气逐小时预报（24–168小时）
- 标识：`/v7/weather/{hours}`，`hours ∈ {24h,72h,168h}`
- 方法：`GET`
- 参数：
  - 必填：`location`
  - 可选：`lang`、`unit`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/weather/24h?location=101010100"
  ```
- 返回（节选）：
  ```json
  {
    "code":"200",
    "hourly":[{"fxTime":"2021-02-16T15:00+08:00","temp":"2","text":"晴","windDir":"西北风","windSpeed":"20","humidity":"11","pop":"0","precip":"0.0","pressure":"1025"}]
  }
  ```
- 参考：https://dev.qweather.com/en/docs/api/weather/weather-hourly-forecast/

---

## 分钟级降水（中国）
- 标识：`/v7/minutely/5m`
- 方法：`GET`
- 参数：
  - 必填：`location`（经纬度）
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/minutely/5m?location=116.38,39.91"
  ```
- 返回（节选）：
  ```json
  {"code":"200","summary":"95分钟后雨就停了","minutely":[{"fxTime":"2021-12-16T18:55+08:00","precip":"0.15","type":"rain"}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/minutely/minutely-precipitation/

---

## 天气指数（生活指数）
- 标识：`/v7/indices/{days}`，`days ∈ {1d,3d}`
- 方法：`GET`
- 参数：
  - 必填：`location`、`type`（指数类型 ID，多个用逗号分隔）
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/indices/1d?type=1,2&location=101010100"
  ```
- 返回（节选）：
  ```json
  {"code":"200","daily":[{"date":"2021-12-16","type":"1","name":"运动指数","level":"3","category":"较不宜","text":"天气较好，但考虑天气寒冷..."}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/indices/indices-forecast/

---

## 空气质量（Air Quality v1）

### 当前空气质量（按经纬度）
- 标识：`/airquality/v1/current/{latitude}/{longitude}`
- 方法：`GET`
- 参数：
  - 路径必填：`latitude`、`longitude`（最多 2 位小数）
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/airquality/v1/current/39.90/116.40"
  ```
- 返回（节选）：
  ```json
  {"metadata":{"tag":"..."},"indexes":[{"code":"us-epa","name":"AQI (US)","aqi":46,"level":"1","category":"Good","primaryPollutant":{"code":"pm2p5"}}],"pollutants":[{"code":"pm2p5","concentration":{"value":11.0,"unit":"μg/m3"}}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/air-quality/air-current/

### 监测站数据（按站点ID）
- 标识：`/airquality/v1/station/{LocationID}`
- 方法：`GET`
- 参数：
  - 路径必填：`LocationID`
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/airquality/v1/station/P53763"
  ```
- 返回（节选）：
  ```json
  {"metadata":{"tag":"...","sources":["..."]},"pollutants":[{"code":"pm2p5","concentration":{"value":11.0,"unit":"μg/m3"}}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/air-quality/air-station/
- 归因：必须完整展示 `metadata.sources`/`refer.sources`

---

## 灾害预警（Warning/Alert）
- 旧版（已废弃）接口：`/v7/warning/now`（保留迁移参考）
- 新版：参考分类页“Warning”中的 Weather Alert 文档
- 示例（旧版）：
  ```json
  {"code":"200","updateTime":"2023-04-03T14:20+08:00","warning":[{"sender":"上海中心气象台","title":"大风蓝色预警","severity":"Minor","severityColor":"Blue","typeName":"大风","text":"..."}]}
  ```
- 归因：必须完整展示 `refer.sources`
- 参考：https://dev.qweather.com/en/docs/api/warning/

---

## 时间机器（近10天历史）
- 标识：`/v7/historical/weather`
- 方法：`GET`
- 参数：
  - 必填：`location`（仅支持 LocationID）、`date`（`yyyyMMdd`，近10天）
  - 可选：`lang`、`unit`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/historical/weather?location=101010100&date=20200725"
  ```
- 返回（节选）：
  ```json
  {"code":"200","weatherDaily":{"date":"2020-07-25","sunrise":"05:08","tempMax":"33","tempMin":"23","precip":"0.0"},"weatherHourly":[{"time":"2020-07-25 00:00","temp":"28","text":"晴","windDir":"西南风"}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/time-machine/time-machine-weather/

---

## 天文（Astronomy）

### 日出日落
- 标识：`/v7/astronomy/sun`
- 方法：`GET`
- 参数：
  - 必填：`location`、`date`
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/astronomy/sun?location=101010100&date=20210220"
  ```
- 返回（节选）：
  ```json
  {"code":"200","sunrise":"2021-02-20T06:58+08:00","sunset":"2021-02-20T17:57+08:00"}
  ```
- 参考：https://dev.qweather.com/en/docs/api/astronomy/sunrise-sunset/

### 月升月落与月相
- 标识：`/v7/astronomy/moon`
- 方法：`GET`
- 参数：
  - 必填：`location`、`date`
  - 可选：`lang`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/astronomy/moon?location=101010100&date=20211120"
  ```
- 返回（节选）：
  ```json
  {"code":"200","moonrise":"2021-11-20T17:25+08:00","moonset":"2021-11-21T07:42+08:00","moonPhase":[{"fxTime":"2021-11-20T00:00+08:00","name":"亏凸月"}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/astronomy/moon-and-moon-phase/

### 太阳高度角与方位角
- 标识：`/v7/astronomy/solar-elevation-angle`
- 方法：`GET`
- 参数：
  - 必填：`location`（经纬度）、`date`（yyyyMMdd）、`time`（HHmm）、`tz`（时区，如 0800/-0530）、`alt`（海拔，米）
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/astronomy/solar-elevation-angle?location=120.34,36.08&alt=43&date=20210220&time=1230&tz=0800"
  ```
- 返回（节选）：
  ```json
  {"code":"200","solarElevationAngle":"42.88","solarAzimuthAngle":"185.92","solarHour":"1217","hourAngle":"-4.41"}
  ```
- 参考：https://dev.qweather.com/en/docs/api/astronomy/solar-elevation-angle/

---

## 热带气旋（台风）

### 台风列表（近两年）
- 标识：`/v7/tropical/storm-list`
- 方法：`GET`
- 参数：
  - 必填：`basin`（如 `NP`），`year`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/tropical/storm-list?basin=NP&year=2024"
  ```
- 返回（节选）：
  ```json
  {"code":"200","storm":[{"id":"NP_2022","name":"环高","basin":"NP","year":"2020","isActive":"0"}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-list/

### 台风路径（活动台风）
- 标识：`/v7/tropical/storm-track`
- 方法：`GET`
- 参数：
  - 必填：`stormid`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/tropical/storm-track?stormid=NP_2021"
  ```
- 参考：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-track/

### 台风预报（指定台风）
- 标识：`/v7/tropical/storm-forecast`
- 方法：`GET`
- 参数：
  - 必填：`stormid`
- 示例：
  ```bash
  curl --compressed \
    -H "X-QW-Api-Key: ${API_KEY}" \
    "https://${API_HOST}/v7/tropical/storm-forecast?stormid=NP_2106"
  ```
- 返回（节选）：
  ```json
  {"code":"200","forecast":[{"fxTime":"2021-07-27T20:00+08:00","lat":"31.7","lon":"118.4","type":"TS","pressure":"990","windSpeed":"18"}]}
  ```
- 参考：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-forecast/

---

## 错误代码对照表（v2）

> 不同接口或错误类型可能返回不同版本；官方正在从 v1 迁移至 v2。出现错误应暂停请求并排查，避免持续错误触发限流或安全策略。

- `400`：INVALID/MISSING PARAMETER/NOT FOUND/DATA NOT AVAILABLE（参数非法/缺失/位置不存在/数据暂不可用）
- `401`：认证失败（检查 KEY 或 JWT）
- `403`：NO CREDIT/OVERDUE/SECURITY RESTRICTION/INVALID HOST/ACCOUNT SUSPENSION/FORBIDDEN（余额/账单/安全限制/Host 无效/账号暂停/无权限）
- `404`：路径或路径参数错误（无响应体）
- `429`：TOO MANY REQUESTS / OVER FREE DAILY LIMIT / OVER MONTHLY LIMIT（QPM/日/月额度超限；需指数退避）
- 官方文档：https://dev.qweather.com/en/docs/resource/error-code/

---

## 调用频率与最佳实践
- 频率限制：与账户套餐及安全策略相关；`429` 表示超限或错误累积，需退避并修正
- Gzip：默认启用，降低带宽 https://dev.qweather.com/en/docs/best-practices/optimize-requests/
- 缓存：除 GeoAPI 外可缓存响应；减少重复请求 https://dev.qweather.com/en/docs/en/docs/help/
- 安全：妥善保管凭据；不在客户端或版本库暴露真实密钥；预警/空气质量需展示来源

---

## 参考索引（保持同步）
- 开发总览：https://dev.qweather.com/en/docs/api/
- Weather 分类页：https://dev.qweather.com/en/docs/api/weather/
- GeoAPI 总览：https://dev.qweather.com/en/docs/api/geoapi/
- Minutely Forecast：https://dev.qweather.com/en/docs/api/minutely/minutely-precipitation/
- Indices Forecast：https://dev.qweather.com/en/docs/api/indices/indices-forecast/
- Air Quality v1：
  - Current：https://dev.qweather.com/en/docs/api/air-quality/air-current/
  - Station：https://dev.qweather.com/en/docs/api/air-quality/air-station/
  - 背景/地区支持：https://dev.qweather.com/en/docs/resource/air-info/
- Warning 分类页：https://dev.qweather.com/en/docs/api/warning/
- Time Machine（天气）：https://dev.qweather.com/en/docs/api/time-machine/time-machine-weather/
- Astronomy：
  - Sun：https://dev.qweather.com/en/docs/api/astronomy/sunrise-sunset/
  - Moon：https://dev.qweather.com/en/docs/api/astronomy/moon-and-moon-phase/
  - Solar Elevation：https://dev.qweather.com/en/docs/api/astronomy/solar-elevation-angle/
- Tropical Cyclone：
  - List：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-list/
  - Track：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-track/
  - Forecast：https://dev.qweather.com/en/docs/api/tropical-cyclone/storm-forecast/

