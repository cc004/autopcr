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

## 运行模式

新版 AutoPCR 使用 [OpenBao](https://openbao.org/) 保存游戏账号密码和 session。两种运行模式都需要预先准备可访问的 OpenBao 服务及认证凭据；AutoPCR 不会启动或解封 OpenBao。认证方式及对应配置见下方「OpenBao 配置」。

### (1)Hoshino 插件模式

请使用最新版 Hoshino，并更新通用配置文件 `config/__bot__.py`。填写OpenBao设置项在Hoshino配置目录下的 `autopcr.py`，也可通过环境变量提供；配置文件优先于环境变量，未设置时使用默认值。配置文件模板见 [`autopcr.py.example`](./autopcr.py.example)。

### (2)单Web服务模式

直接运行 HTTP 服务时，使用以下命令启动：

```bash
python3 httpserver_standalone.py
```

OpenBao 配置可通过启动参数或环境变量提供，优先级为启动参数 > 环境变量 > 默认值。启动参数可用 `--openbao-*` 形式传入，完整选项可运行 `python3 httpserver_standalone.py --help` 查看。

## OpenBao 配置

`AUTOPCR_OPENBAO_AUTH_METHOD` 支持 `approle`、`token` 和 `kubernetes`。应用启动时会连接 OpenBao 并验证凭据；认证失败或 OpenBao 不可用会导致启动失败。AppRole 推荐用于服务部署；静态 Token 只从文件读取、不自动续期，其有效期和轮换由管理员管理。

**AppRole（推荐用于服务部署）**

```python
AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"  # OpenBao 服务地址
AUTOPCR_OPENBAO_AUTH_METHOD = "approle"  # 认证方式：AppRole
AUTOPCR_OPENBAO_ROLE_ID = "your-role-id"  # AppRole 的 Role ID
AUTOPCR_OPENBAO_SECRET_ID_FILE = "/path/to/openbao/secret-id"  # 存放 Secret ID 的受限权限文件
AUTOPCR_OPENBAO_APPROLE_MOUNT = "approle"  # AppRole auth method 的挂载名称
```

如果希望把 Role ID 也放入文件，可用 `AUTOPCR_OPENBAO_ROLE_ID_FILE`（Role ID 文件路径）；不设置 `AUTOPCR_OPENBAO_ROLE_ID` 时会从该文件读取。

**静态 Token**

```python
AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"  # OpenBao 服务地址
AUTOPCR_OPENBAO_AUTH_METHOD = "token"  # 认证方式：静态 Token
AUTOPCR_OPENBAO_TOKEN_FILE = "/path/to/openbao/app-token"  # 存放 Token 的受限权限文件
```

**Kubernetes**

```python
AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"  # OpenBao 服务地址
AUTOPCR_OPENBAO_AUTH_METHOD = "kubernetes"  # 认证方式：Kubernetes ServiceAccount
AUTOPCR_OPENBAO_K8S_ROLE = "autopcr"  # OpenBao 中绑定该 ServiceAccount 的 Kubernetes auth role
AUTOPCR_OPENBAO_K8S_MOUNT = "kubernetes"  # Kubernetes auth method 的挂载名称
AUTOPCR_OPENBAO_K8S_JWT_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/token"  # Pod 内 ServiceAccount JWT 文件
```

## 容器部署（直接提供的镜像仅适用于运行单Web服务模式，Hoshino插件模式请自行构建镜像）

数据持久化通过 Docker named volumes 实现：

| 卷名 | 容器路径 | 说明 |
|------|---------|------|
| `autopcr_cache` | `/app/cache` | 用户身份数据库、游戏账号配置、游戏数据库；不存储游戏登录 session |
| `autopcr_result` | `/app/result` | 任务执行结果 |
| `autopcr_log` | `/app/log` | 应用日志 |
| `autopcr_audit` | `/app/audit` | AutoPCR OpenBao 操作日志 |

### (1)使用本机 Openbao 的 Compose 部署

#### 一键启动

单机 Compose 包含 OpenBao 服务端、负责持续检查/解封的 `openbao-init` supervisor，以及配置 KV 引擎/策略/AppRole 凭据的一次性 `openbao-bootstrap`。OpenBao 使用原生 file audit device 记录 API 请求和响应，bootstrap 成功退出后，日常解封由 `openbao-init` 负责；AutoPCR 使用 AppRole 获取并续租登录 token。OpenBao API 不对宿主机发布端口。

启动服务：

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

OpenBao 使用 Shamir 5 份、阈值 3 的初始化密钥。`openbao-init` 会将完整初始化结果一次性保存为 `recovery.json`，并在每次解封时逐份提交 key，达到 3 份阈值后停止。Raft 数据、初始化恢复文件、root token 交接文件、应用凭据分别保存在 `autopcr_openbao_data`、`autopcr_openbao_keys`、`autopcr_openbao_bootstrap`、`autopcr_openbao_token` 卷中。完整的 5 份 key 都保存在 `recovery.json`，所以本机自动解封方便，但 3/5 阈值本身不构成对 Docker 宿主机或密钥卷失陷的额外保护。只有 `openbao-init` 挂载密钥卷；root token 交接卷只读挂载给 `openbao-bootstrap`；应用容器只读挂载应用凭据卷。

**首次启动后请立即导出并妥善保存 recovery 文件**：其中包含全部 5 份解封密钥和初始 root token。将文件加密后保存到密码管理器或其他主机/离线介质，再删除导出的明文副本。它不是 Raft 数据备份，完整灾难恢复仍需与之匹配的 Raft 数据备份。

#### 导出恢复文件:

```bash
sh docker/openbao-recovery.sh export ./openbao-recovery.json
```

#### 备份与恢复

本机 OpenBao 使用 Raft。使用仓库脚本备份时，会暂时停止 AutoPCR、bootstrap、init supervisor 和 OpenBao，再将 Raft 数据卷与对应的初始化密钥卷一起归档；完成后会恢复备份前正在运行的服务。该备份包含 Raft 数据、全部解封密钥和初始 root token，必须加密并保存到主机之外：

```bash
sh docker/openbao-recovery.sh backup ./openbao-backup
```

在新主机恢复时，先把备份目录放到仓库中，在启动 Compose 服务前执行：

```bash
sh docker/openbao-recovery.sh restore ./openbao-backup
docker compose up -d
```

恢复会同时写入 Raft 数据和与其匹配的初始化密钥，并移除旧的一次性 bootstrap 容器，使下次启动重新 reconcile KV、策略和 AppRole 凭据。目标卷非空时脚本拒绝覆盖；只有确认要替换卷内容时才传入 `--force`。不要只恢复初始化密钥到空 Raft 卷：`openbao-init` 检测到“Raft 尚未初始化但已有密钥材料”会拒绝重新初始化，避免意外创建新集群覆盖恢复流程。单独保留 recovery 文件不能恢复已丢失的 Raft 数据。

如果 Compose 项目使用了 `-p` 或 `COMPOSE_PROJECT_NAME` 自定义项目名，运行恢复脚本时也要设置相同的 `COMPOSE_PROJECT_NAME`，以便定位对应的数据卷和密钥卷。

### (2)使用外部 OpenBao 的 Compose 配置

#### 自动 bootstrap 并取得凭据

外部 OpenBao 需已完成初始化并处于解封状态。按[外部 OpenBao 教程](./OPENBAO.md)运行第一个脚本，创建专用于 bootstrap 的 `admin-token` 和 `ready` 标记；不要直接使用 root token。管理机器需安装 OpenBao CLI（`bao`）和 Python 3。将包含这两个文件的目录提供给 `AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR`：

```bash
export AUTOPCR_OPENBAO_ADDR="https://openbao.example.com:8200"
export AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR="/secure/path/openbao-admin"
docker compose -f docker-compose.yml -f docker-compose.auto-bootstrap up -d
```

该覆盖不会启动本地 OpenBao 或初始化/解封服务；一次性 bootstrap 容器会只读挂载该目录，从 `admin-token` 读取 `admin_token`，并检查 `ready` 标记。之后它会在外部 OpenBao 上创建 `autopcr/` KV v2、最小权限策略及 AppRole，再把 AutoPCR 专用凭据和运行就绪标记写入 Docker 命名卷。AutoPCR 只使用 AppRole 凭据，不会接触 `admin_token`。外部 OpenBao 必须在启动 Compose 前已可访问且已解封；本地数据卷会保留生成的 AppRole 凭据。

#### 手动 bootstrap 并提供凭据

外部 OpenBao 需已完成初始化并处于解封状态。按 [外部 OpenBao 教程](./OPENBAO.md)的手动配置部分完成 OpenBao 配置，并按选择的认证方式准备应用凭据：AppRole 需要 Secret ID（文件）和 Role ID（文件或环境变量）；静态 Token 需要 token 文件。第三个脚本把 AppRole 凭据和 `ready` 写入 `AUTOPCR_OPENBAO_APP_TOKEN_DIR`；这个目录中的 `ready` 表示应用凭据已就绪，与 admin token 目录中的 bootstrap `ready` 含义不同。只将 AutoPCR 应用凭据放入单独的宿主机目录，不要把包含 `admin-token` 的目录挂载给 AutoPCR。设置 OpenBao 地址及凭据目录，并用手动配置的 Compose 文件启动：

```bash
export AUTOPCR_OPENBAO_ADDR="https://openbao.example.com:8200"
export AUTOPCR_OPENBAO_AUTH_DIR="/secure/path/autopcr-openbao"
# AppRole 为默认认证方式；如改用静态 Token，取消下一行注释
# export AUTOPCR_OPENBAO_AUTH_METHOD="token"
# Role ID 可由 /secure/path/autopcr-openbao/role-id 文件提供；
# 也可取消下一行注释，直接通过环境变量设置
# export AUTOPCR_OPENBAO_ROLE_ID="your-role-id"
docker compose -f docker-compose.yml -f docker-compose.manual-bootstrap.yml up -d
```

使用 AppRole 时，凭据目录需包含 `secret-id`，Role ID 可放在同目录的 `role-id` 文件中，或通过 `AUTOPCR_OPENBAO_ROLE_ID` 提供。使用静态 Token 时，目录需包含 `app-token` 文件。手动配置默认使用 `approle` mount；如使用自定义 mount，启动 Compose 时需设置相同的 `AUTOPCR_OPENBAO_APPROLE_MOUNT`。保护好凭据文件；管理员 token 不需要提供给 AutoPCR。

### (3)使用Kubenetes集群

```python
AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"
AUTOPCR_OPENBAO_AUTH_METHOD = "kubernetes"
AUTOPCR_OPENBAO_K8S_ROLE = "autopcr"
AUTOPCR_OPENBAO_K8S_MOUNT = "kubernetes"
AUTOPCR_OPENBAO_K8S_JWT_FILE = "/var/run/secrets/kubernetes.io/serviceaccount/token"
```

Kubernetes 模式使用 Pod ServiceAccount JWT 登录 OpenBao。OpenBao 管理员需预先启用并配置 Kubernetes auth method、绑定相应 ServiceAccount/namespace 的 role，并授予 AutoPCR policy；AutoPCR 本身不会配置集群或 OpenBao 的 Kubernetes auth。

## 使用外部 OpenBao

外部 OpenBao 的初始化、解封、策略配置及 AutoPCR 凭据获取步骤请参阅[使用外部 OpenBao](./OPENBAO.md)。

## 新版数据存储与旧数据迁移

用户身份、登录密码哈希、用户与游戏账号名的对应关系及批量账号选择保存在 `/app/cache/http_server/users.db`；批量运行的结果索引和配置保留在 `BATCH_RUNNER.json`；游戏账号凭据及登录后取得的凭据保存在 OpenBao。普通账号 JSON 仅保留服务器类型、任务选项、运行结果等非敏感配置。

启动时会迁移旧版 `secret`、旧账号 JSON 中的游戏账号密码及 `BATCH_RUNNER.json` 中的批量账号选择。写入目标存储成功后，会清空旧 JSON 中的批量账号选择和凭据字段，并保留其结果及配置；只有 OpenBao 写入成功后才删除旧明文文件。迁移失败会报错并保留旧文件供恢复。

## 配置一览

常规部署可通过环境变量配置，Docker 部署时在 `.env` 文件中设置即可，参见 `.env.example`；Hoshino 插件模式也可在 `config/autopcr.py` 中配置 OpenBao 相关选项。

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| AUTOPCR_SERVER_HOST | 服务器绑定地址 | 0.0.0.0 |
| AUTOPCR_SERVER_PORT | 服务器启动端口 | 13200 |
| AUTOPCR_SERVER_DEBUG_LOG | 是否输出 Debug 日志 | False |
| AUTOPCR_SERVER_ALLOW_REGISTER | 是否允许注册 | True |
| AUTOPCR_SERVER_SUPERUSER | 设置无条件拥有管理员的用户 | （可选，设置为登录使用的 QQ） |
| AUTOPCR_PUBLIC_ADDRESS | QQ bot 发送的公网访问地址 | （可选，留空自动检测） |
| AUTOPCR_USE_HTTPS | 公网访问链接是否使用 HTTPS | False |
| AUTOPCR_OPENBAO_ADDR | OpenBao API 地址 | `http://127.0.0.1:8200` |
| AUTOPCR_OPENBAO_AUTH_METHOD | OpenBao 认证方式：`token`、`approle` 或 `kubernetes` | 直接运行默认 `token`；本机 Docker Compose 默认 `approle` |
| AUTOPCR_OPENBAO_TOKEN_FILE | 静态应用 token 文件；token 模式必填，需自行提供 | 缓存目录下的 `openbao/app-token` |
| AUTOPCR_OPENBAO_ROLE_ID | AppRole Role ID；可由文件提供 | 空 |
| AUTOPCR_OPENBAO_ROLE_ID_FILE | AppRole Role ID 文件 | 缓存目录下的 `openbao/role-id` |
| AUTOPCR_OPENBAO_SECRET_ID_FILE | AppRole Secret ID 文件 | 缓存目录下的 `openbao/secret-id` |
| AUTOPCR_OPENBAO_APPROLE_MOUNT | AppRole auth mount 名称 | `approle` |
| AUTOPCR_OPENBAO_K8S_ROLE | Kubernetes auth role | 空（Kubernetes 模式必填） |
| AUTOPCR_OPENBAO_K8S_MOUNT | Kubernetes auth mount 名称 | `kubernetes` |
| AUTOPCR_OPENBAO_K8S_JWT_FILE | Kubernetes ServiceAccount JWT 文件 | `/var/run/secrets/kubernetes.io/serviceaccount/token` |

以下为 容器 部署专属变量（在 `docker-compose.yml` 中使用）：

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| HOST_PORT | 宿主机映射端口 | 13200 |
| TZ | 容器时区 | Asia/Shanghai |
| RESTART_POLICY | 容器重启策略 | unless-stopped |
| AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR | 使用外部 OpenBao 的 Compose 覆盖时，包含 `admin-token` 和 `ready` 文件的宿主机目录；仅挂载给一次性 bootstrap 容器 | 必填 |

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

若使用外部静态 Token，启动前设置环境变量，例如 PowerShell：

```powershell
$env:AUTOPCR_OPENBAO_AUTH_METHOD = "token"
$env:AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"
$env:AUTOPCR_OPENBAO_TOKEN_FILE = "C:\secrets\openbao\app-token"
pixi run server
```
