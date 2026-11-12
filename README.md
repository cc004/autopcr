# autopcr

[![License](https://img.shields.io/github/license/cc004/autopcr)](LICENSE)

自动清日常
bug反馈/意见/交流群: 885228564

请先运行一次`python3 _download_web.py`下载前端资源。

如果网络不好，可自行[下载压缩包](https://github.com/Lanly109/AutoPCR_Web/releases/latest)，然后`python3 _download_web.py /path/to/zip`安装。

可再运行`python3 _download_data.py`下载数据库和图片资源。

## 渠道服支持

渠道服需要自抓`uid`和`access_key`，作为用户名和密码。

## Web界面访问

访问路径为`/daily/login`。

## 凭据存储

默认**明文**保存游戏账号相关信息。可选择存入[OpenBao](https://openbao.org/) 保护游戏账号凭据。详细配置和部署说明见[OpenBao 文档](./openbao/OPENBAO.md)。

## 运行模式

### (1)Hoshino 插件模式

请使用最新版 Hoshino，并更新通用配置文件 `config/__bot__.py`。

### (2)单Web服务模式

直接运行 HTTP 服务时，使用以下命令启动：

```bash
python3 httpserver_standalone.py
```

## 容器部署（项目提供Package仅适用于运行单Web服务模式，Hoshino插件模式请自行构建镜像）

数据持久化通过 Docker named volumes 实现：

| 卷名 | 容器路径 | 说明 |
|------|---------|------|
| `autopcr_cache` | `/app/cache` | 用户身份数据库、游戏账号配置和本地 session 文件 |
| `autopcr_result` | `/app/result` | 任务执行结果 |
| `autopcr_log` | `/app/log` | 应用日志 |

## 新版数据存储与旧数据迁移

用户身份、登录密码、用户名下游戏账号昵称、以及批量账号的选择信息保存在 `/app/cache/http_server/users.db`；批量运行的结果索引和配置保留在 `BATCH_RUNNER.json`。

启动时会自动迁移旧版本 `secret` 和 `BATCH_RUNNER.json` 中的批量账号选择信息。

## 配置一览

常规部署可通过环境变量配置，Docker 部署时在 `.env` 文件中设置即可，参见 `.env.example`。

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| AUTOPCR_SERVER_HOST | 服务器绑定地址 | 0.0.0.0 |
| AUTOPCR_SERVER_PORT | 服务器启动端口 | 13200 |
| AUTOPCR_SERVER_DEBUG_LOG | 是否输出 Debug 日志 | False |
| AUTOPCR_SERVER_ALLOW_REGISTER | 是否允许注册 | True |
| AUTOPCR_SERVER_SUPERUSER | 设置无条件拥有管理员的用户 | （可选，设置为登录使用的 QQ） |
| AUTOPCR_PUBLIC_ADDRESS | QQ bot 发送的公网访问地址 | （可选，留空自动检测） |
| AUTOPCR_USE_HTTPS | 公网访问链接是否使用 HTTPS | False |

以下为容器部署专属变量（在 `docker-compose.yml` 中使用）：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| HOST_PORT | 宿主机映射端口 | 13200 |
| TZ | 容器时区 | Asia/Shanghai |
| RESTART_POLICY | 容器重启策略 | unless-stopped |

## Credits
- aiorequests 来自 [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)
- 图片绘制改自 [convert2img](https://github.com/SonderXiaoming/convert2img)
- 前端html来自 [AutoPCR_Web](https://github.com/Lanly109/AutoPCR_Web)
- 角色OCR来自 [arena](https://github.com/watermellye/arena)
- ~~前端html来自 [autopcr_web](https://github.com/cca2878/autopcr_web)~~
- ~~前端html来自 [AutoPCR_Archived](https://github.com/watermellye/AutoPCR_Archived)~~
- ~~模型生成来自 [PcrotoGen](https://github.com/cc004/PcrotoGen)~~

## Github Action（Action打包镜像运行于单Web服务模式）
打包镜像默认推送到[ghcr](https://ghcr.io),如需推送到[dockerhub](https://hub.docker.com)需要执行以下步骤
- 添加变量`DOKCKERHUB_IMAGE_NAME`用于推送到dockerhub镜像名称,例如autopcr/autopcr
- 添加机密`DOCKERHUB_USERNAME`和`DOCKERHUB_TOKEN`用于推送到dockerhub的身份验证

## 使用 pixi 启动单Web服务

创建环境：`pixi install`
下载前端资源：`pixi run download_web`
启动服务器：`pixi run server`（等同于运行 `python3 httpserver_standalone.py`，使用单Web服务模式配置）。
