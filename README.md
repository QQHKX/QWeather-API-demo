# QWeather API 演示项目

本项目基于和风天气官方文档，实现统一的 Python 客户端与完整示例、测试与文档，覆盖 GeoAPI、天气实况/预报、分钟级降水、指数、空气质量（v1）、预警、时间机器、天文、热带气旋等主要接口。

## 安装

- 需要 Python 3.8+
- 推荐使用 `uv` 管理依赖与虚拟环境；如未安装 `uv`，请在 Windows PowerShell 执行：

```powershell
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
```

创建虚拟环境并同步依赖（包含开发依赖）：

```powershell
uv venv
uv sync --all-extras
```

如果网络较慢，建议使用国内镜像源（临时生效示例）：

```powershell
$env:UV_INDEX_URL = 'https://pypi.tuna.tsinghua.edu.cn/simple'
$env:UV_HTTP_TIMEOUT = '120'
uv sync --all-extras
```

也可以使用阿里云镜像：

```powershell
$env:UV_INDEX_URL = 'https://mirrors.aliyun.com/pypi/simple/'
uv sync --all-extras
```

若暂未安装 `uv`，也可使用 `pip` 作为后备：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 配置

在项目根目录创建 `.env`（已加入 `.gitignore`，不会被提交）。可参考仓库提供的 `.env.example`：

```
API_HOST=你的控制台给出的主机名
API_KEY=你的API密钥（或使用 JWT_TOKEN）
# JWT_TOKEN=你的JWT令牌（可选，优先于 API_KEY）
```

## 快速开始

以“天气实况”为例：

```powershell
uv run python examples/example_weather_now.py
```

更多示例位于 `examples/` 目录，均会演示初始化、参数设置、结果展示与错误处理。

## 项目结构

- `src/qweather_client/`：统一客户端与各 API 模块
- `examples/`：覆盖所有 API 的演示脚本
- `tests/`：单元测试与异常场景覆盖
- `docs/`：每个 API 的详细使用说明

## 运行测试（包含覆盖率）

```powershell
uv run pytest
```

已配置 `--cov-fail-under=90`，确保覆盖率不低于 90%。

## 类型检查

```powershell
uv run mypy src
```

## Git 管理与推送指南

- 已提供标准 `.gitignore`，确保 `.env`、虚拟环境与本地构建产物不被提交。
- 已添加 `.gitattributes` 保持跨平台行尾一致（源码统一 LF）。
- 如误将 `.env` 加入暂存区，可执行：
  ```powershell
  git rm --cached .env
  ```
- 推荐推送前进行质量检查：
  ```powershell
  uv run pytest
  uv run mypy src
  ```
- 推送到 GitHub（示例）：
  ```powershell
  git init
  git add .
  git commit -m "feat: 初始化 QWeather 演示项目"
  git branch -M main
  git remote add origin https://github.com/<your-user>/<your-repo>.git
  git push -u origin main
  ```

## 许可与归因

使用和风天气数据需在产品界面注明“天气服务由和风天气驱动”并链接 https://www.qweather.com ，并按官方要求展示来源字段。
