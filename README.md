# autopcr

[![License](https://img.shields.io/github/license/cc004/autopcr)](LICENSE)

自动清日常
bug反馈/意见/交流群: 885228564

请先运行一次`python3 _download_web.py`下载前端资源。

如果网络不好，可自行[下载压缩包](https://github.com/Lanly109/AutoPCR_Web/releases/latest)，然后`python3 _download_web.py /path/to/zip`安装。

可再运行`python3 _download_data.py`下载数据库和图片资源。

## HTTP 服务器模式

```bash
python3 _httpserver_test.py
```

访问`/daily/login`

## Hoshino插件模式

使用前请更新Hoshino到最新版，并**更新Hoshino的配置文件`__bot__.py`**

## 渠道服支持

渠道服需要自抓`uid`和`access_key`，作为用户名和密码。

## 台服支持

台服使用的是游戏会话凭据，不是 So-net 账号密码。需要准备以下字段：

| 字段 | 说明 |
|------|------|
| `SHORT_UDID` | 作为 autopcr 的“用户名” |
| `UDID` | 32 位十六进制或带横线的 36 位 UUID |
| `VIEWER_ID` | 游戏账号的数字 ID |
| `TW_SERVER_ID` | 分区编号，只能为 `1`、`2`、`3` 或 `4` |
| `APP_VERSION` | 可选的单账号客户端版本；留空时使用环境变量或程序默认值 |

网页端只有用户名和密码输入框时，平台选择“台服”，用户名填写 `SHORT_UDID`，密码按以下格式填写：

```text
UDID:VIEWER_ID:TW_SERVER_ID
```

例如：`00112233-4455-6677-8899-aabbccddeeff:1123456789:1`。通过后端接口或账号 JSON 配置时，也可以把 `viewer_id`、`server_id` 和可选的 `app_version` 作为独立字段保存，此时 `password` 只需填写 `UDID`。

批量导入 TSV 的字段顺序为：

```text
昵称<TAB>SHORT_UDID<TAB>UDID<TAB>台服<TAB>VIEWER_ID<TAB>TW_SERVER_ID<TAB>APP_VERSION
```

最后一列 `APP_VERSION` 可省略，TSV 不要添加表头。

程序当前默认使用 `APP_VERSION=5.7.0`（截至 2026-07-15 的[台服官方 5.7.0 公告](https://www.princessconnect.so-net.tw/news/newsDetail/3854)和 [Google Play](https://play.google.com/store/apps/details?id=tw.sonet.princessconnect) 版本）；Android 5.7.0 包内运行时为 `Unity 6000.0.58f2`、`libcurl 8.10.1-DEV`，服务端当前要求的 HTTP 资源版本为 `00500030`。后续客户端升级时可通过下方环境变量覆盖，无需修改国服配置。HTTP `RES-VER` 与 master database 版本是两个独立的版本号，不能相互替代。

Android 5.7.0 的 base APK（SHA-256 `731077aeb6335bd9be233dde8948d76c4e36f72db348d19a82cf13e58856baea`）已通过官方 `apksigner` 的 v2/v3 校验；签名证书 SHA-1 为 `7e7693f1fdf57cb845f09080a761da5f4ce4cb2f`。项目已按该包的 IL2CPP metadata v31 对当前开放的登录/日常请求做字段和类型比对：`ApiManager` 路径的 58 个请求、121 个业务字段一致。台服专有响应字段会被保留并参与本地库存、钻石等状态更新。

### 从 Android PlayerPrefs 提取凭据

将台服客户端的 PlayerPrefs XML 复制到本机后，在项目根目录运行：

```bash
python -m autopcr.sdk.twplayerprefs "/path/to/playerprefs.xml" --alias "台服账号"
```

命令会输出一行可直接导入的 TSV（默认不包含可选的 `APP_VERSION` 列）。请只在可信设备上本地执行；输出、原 XML 和账号缓存都包含可直接使用的会话凭据，不要上传、分享、写入日志或提交到 Git，导入后应及时删除临时 TSV。

### 数据库与支持范围

台服登录在 `game_start` 返回权威 `required_res_ver` 后，会优先读取 So-net 官方资源清单，依次解析根清单、`masterdata*_assetmanifest` 和内容寻址 pool，下载 `a/masterdata_master.unity3d`，再提取其中的 `master` TextAsset。该链路对照了 [unity-texture-toolkit 的台服实现](https://github.com/esterTion/unity-texture-toolkit/blob/138aa6a9bda38a98dc247942cfb4ab1d4026619f/tw_redive/main.php#L317)、[redive_linebot 的官方资源配置](https://github.com/hanshino/redive_linebot/blob/527331002cab355f1735b4cd08b3d02e002fdf83/tools/tw-redive-db-fetcher/config.py#L4)及其[数据库抓取实现](https://github.com/hanshino/redive_linebot/blob/527331002cab355f1735b4cd08b3d02e002fdf83/tools/tw-redive-db-fetcher/main.py)。Unity 6000 的 bundle 无需额外密钥，但必须使用 `UnityPy >= 1.25.0`；旧版 1.10 会误判资源标志。

官方 SQLite 会用 `data/rainbow_tw.json` 严格还原 939 张已映射表及其列名，完成必需表检查和 `PRAGMA quick_check` 后才原子写入 `cache/db/tw/official/`。2026-07-15 实测资源版本 `00500030` 解码后为 45,641,728 字节、947 张表。官方更新失败时才使用 [Expugn/priconne-database](https://github.com/Expugn/priconne-database) 的已解码镜像；官方与镜像缓存相互隔离，镜像再按上游 hash 分代，加载成功后保留当前文件和一个回退文件，避免 Windows 覆盖已打开 SQLite 以及长期无限堆积。程序默认每小时检查版本，回退后最多 5 分钟再尝试官方源，所有下载均有大小上限。

首次从官方 AssetBundle 提取数据库时，UnityPy 会有明显的瞬时内存开销：对 `00500030` 的独立实测峰值约 410 MiB。运行完整服务时建议至少预留 1 GiB 可用内存；低内存设备可设置 `AUTOPCR_TW_OFFICIAL_DB=false`，跳过本地 Unity 解包并直接使用已解码镜像。后续启动会复用已校验的 SQLite 缓存，不会每次重复解包。

台服账号当前开放 120 个已审计模块，除原有基础日常外，还包括旅行、额外装备、商队、深域、属性强化及相关规划工具。究极炼成的台服 `exec_type` 和赛季通行证的 `battlepass/*` 端点使用区域专用请求体，国服仍保持原协议分支。当前仍隐藏 `monthly_gacha`、`set_my_party`、`unit_memory_buy_batch`、`unit_promote_batch` 和 `get_box_table`；活动和客户端更新仍可能带来协议变化。

本次适配已使用本地 PlayerPrefs 完成真实服务器的 `check_agreement → game_start → load/index → home/index → daily_task/top` 登录验证，并使用 Web 导出的完整配置执行过台服日常队列。切换到官方 `00500030` 数据库后，又定向复测了全局设置、家园点赞、礼物、地下城、智能 Hard、活动 Hard、活动箱兑换和赛季通行证；已完成项目会按预期安全跳过。真实清日常会领取、扫荡、抽卡或消费游戏内资源，仍建议先用单个账号和少量低风险任务试运行，再逐步启用完整配置。

## Docker 部署

```bash
# 1. 复制环境变量模板并按需修改
cp .env.example .env

# 2. 一键启动
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务（数据不会丢失）
docker compose down
```

数据持久化通过 Docker named volumes 实现，以下目录会被持久化保存：

| 卷名 | 容器路径 | 说明 |
|------|---------|------|
| `autopcr_cache` | `/app/cache` | 用户账号配置、游戏数据库、session |
| `autopcr_result` | `/app/result` | 任务执行结果 |
| `autopcr_log` | `/app/log` | 应用日志 |

## 配置

所有配置均可通过环境变量控制，Docker 部署时在 `.env` 文件中设置即可，参见 `.env.example`。

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| AUTOPCR_SERVER_HOST | 服务器绑定地址 | 0.0.0.0 |
| AUTOPCR_SERVER_PORT | 服务器启动端口 | 13200 |
| AUTOPCR_SERVER_DEBUG_LOG | 是否输出 Debug 日志 | False |
| AUTOPCR_SERVER_ALLOW_REGISTER | 是否允许注册 | True |
| AUTOPCR_SERVER_SUPERUSER | 设置无条件拥有管理员的用户 | （可选，设置为登录使用的 QQ） |
| AUTOPCR_PUBLIC_ADDRESS | QQ bot 发送的公网访问地址 | （可选，留空自动检测） |
| AUTOPCR_USE_HTTPS | 公网访问链接是否使用 HTTPS | False |
| AUTOPCR_TW_APP_VERSION | 台服默认客户端版本；台服更新后可覆盖 | 5.7.0 |
| AUTOPCR_TW_RES_VERSION | 台服 HTTP 资源版本兜底值；与 master database 版本相互独立，响应后按服务端要求刷新 | 00500030 |
| AUTOPCR_TW_UNITY_VERSION | 台服 Unity 请求头版本 | 6000.0.58f2 |
| AUTOPCR_TW_CURL_VERSION | 台服 User-Agent 中的 libcurl 版本 | 8.10.1-DEV |
| AUTOPCR_TW_USE_SYSTEM_PROXY | 是否让台服请求读取系统代理；默认直连，确需代理时开启 | false |
| AUTOPCR_TW_DEVICE_ID | 可选的台服稳定设备标识；留空时按各账号 UDID 派生 | （可选） |
| AUTOPCR_TW_API_ROOT | 台服 API 根地址覆盖；一般留空 | （可选） |
| AUTOPCR_TW_OFFICIAL_DB | 是否优先从 So-net 官方资源清单自动更新数据库 | true |
| AUTOPCR_TW_RESOURCE_BASE_URL | 台服官方资源服务器根地址 | https://img-pc.so-net.tw |
| AUTOPCR_TW_DB_CHECK_INTERVAL | 台服数据库版本检查间隔（秒，最小 60） | 3600 |
| AUTOPCR_TW_DB_VERSION_URL | 台服镜像回退版本 JSON；一般无需修改 | Expugn raw URL |
| AUTOPCR_TW_DB_URL | 台服镜像回退 `master_tw.db`；一般无需修改 | Expugn raw URL |

以下为 Docker 部署专属变量（仅在 `docker-compose.yml` 中使用）：

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
- 台服协议实现 [pcrjjc_tw_new](https://github.com/azmiao/pcrjjc_tw_new)、[kanna_connection_redive_2](https://github.com/SonderXiaoming/kanna_connection_redive_2)、[nowem](https://github.com/TWT233/nowem)、[3333](https://github.com/duoshoumiao/3333)
- 台服资源更新链路[unity-texture-toolkit](https://github.com/esterTion/unity-texture-toolkit)、 [redive_linebot](https://github.com/hanshino/redive_linebot)

## Github Action（打包镜像仅适用于HTTP服务器模式）
打包镜像默认推送到[ghcr](https://ghcr.io),如需推送到[dockerhub](https://hub.docker.com)需要执行以下步骤
- 添加变量`DOKCKERHUB_IMAGE_NAME`用于推送到dockerhub镜像名称,例如autopcr/autopcr
- 添加机密`DOCKERHUB_USERNAME`和`DOCKERHUB_TOKEN`用于推送到dockerhub的身份验证

## 使用 pixi

创建环境：`pixi install`
下载前端资源：`pixi run download_web`
启动服务器：`pixi run server`
