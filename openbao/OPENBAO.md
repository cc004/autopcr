# OpenBao 配置与部署

支持选用[OpenBao](https://openbao.org/) 作为游戏账号凭据存储。启用 OpenBao 后，应用启动时会连接并验证 OpenBao，认证失败或服务不可用会导致初始化失败。认证成功后，账号密码和 session 会迁入 OpenBao。当目标数据写入并验证成功后，账号 JSON 中的凭据会被清理，session 文件也会被删除。迁移失败时则会保留源文件。不支持将 OpenBao 中的数据重新迁移回明文存储。

请在启用OpenBao前备份`/cache`目录。

## 单机自动部署与配置 Openbao(受项目提供Package所限，适用于运行单Web服务模式)

### 一键启动

```bash
cd openbao
```

先复制环境变量模板：

```bash
cp .env.example .env
```

按需修改环境变量后，执行以下命令。

```bash
docker compose up -d
```

该部署包含 OpenBao、初始化/解封 supervisor（自动解封）、一次性 bootstrap 和 AutoPCR。
自动初始化使用 Shamir 5 份密钥、阈值 3；

### 恢复与备份

首次启动后，立即导出并妥善保存 recovery 文件：包含全部解封密钥和初始 root token。

```bash
sh scripts/openbao-recovery.sh export ./openbao-recovery.json
```

本机 OpenBao 使用 Raft。备份时会暂时停止服务，再一起归档 Raft 数据和匹配的初始化密钥：

```bash
sh scripts/openbao-recovery.sh backup ./openbao-backup
```

恢复前停止 Compose 服务，在仓库根目录运行：

```bash
docker compose down
sh scripts/openbao-recovery.sh restore ./openbao-backup
docker compose up -d
```

目标卷非空时脚本拒绝覆盖；确认要替换卷内容时才传入 `--force`。若使用自定义 `COMPOSE_PROJECT_NAME`，启动 Compose 和运行恢复脚本时都必须设置相同的名称。

## 使用自定义 OpenBao 并完成初始化与 Bootstrap(Hoshino插件模式需要)

执行以下命令需安装 [OpenBao CLI（`bao`）](https://github.com/openbao/openbao/releases)和 Python 3。

### 1.初始化与解封

可通过以下命令启动一个本地OpenBao容器实例。

```bash
cd openbao
docker compose -f docker-compose.openbao.yml up -d
docker compose -f docker-compose.openbao.yml ps
```

若使用上述本地容器，将 `BAO_ADDR` 设为本地地址；

```bash
export BAO_ADDR="http://127.0.0.1:8200"
```

若连接其他 OpenBao，则替换为对应地址。

```bash
export BAO_ADDR="https://openbao.example.com:8200"
```

**http(s)不可省略**

有了OpenBao实例后，对尚未初始化的集群执行以下命令。使用 Shamir seal，生成 5 份解封密钥、阈值为 3：

```bash
umask 077
bao operator init -key-shares=5 -key-threshold=3 -format=json > /tmp/openbao-init-result.json
```

将初始化结果备份到安全位置。它包含 root token 和解封密钥。

使用 `openbao-init-result.json` 中的任意 **3 份不同的** `unseal_keys_b64` 来解封。

```sh
bao operator unseal
# 按提示输入第 1 份 unseal key
bao operator unseal
# 按提示输入第 2 份不同的 unseal key
bao operator unseal
# 按提示输入第 3 份不同的 unseal key
bao status
```

确认 `bao status` 显示 `Sealed` 为 `false`。

**注意每次OpenBao服务重启或重新封存后都需要重新解封**。

### 2.Bootstrap

先从初始化结果中读取 root token 并设置 `BAO_TOKEN`，供管理脚本使用；不要将 token 明文写入命令历史：

```bash
export OPENBAO_ROOT_TOKEN="$(sed -n 's/.*"root_token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' /tmp/openbao-init-result.json)"
export BAO_TOKEN="$OPENBAO_ROOT_TOKEN"
```

运行 [`01-create-admin-token.sh`](./scripts/extras/01-create-admin-token.sh)，默认在`/run/openbao/admin`创建 `admin-token` 和 `ready` 标记。

运行 [`02-setup-autopcr-kv.sh`](./scripts/extras/02-setup-autopcr-kv.sh)，创建或校验 KV v2 mount 和应用策略。

之后按需选择认证方式：

- **AppRole（推荐）**：运行 [`03-setup-autopcr-approle.sh`](./scripts/extras/03-setup-autopcr-approle.sh)。默认脚本将 Role ID、Secret ID 和 `ready` 写入`/run/openbao/app`目录下。
- 
- **静态 Token**：运行 [`04-create-autopcr-static-token.sh`](./scripts/extras/04-create-autopcr-static-token.sh)。该脚本创建仅附加 `autopcr` 策略、有效期 30 天且不可续期的 Token，默认写入`/run/openbao/app/app-token`文件。Token 过期或怀疑泄露时需管理员撤销并重新签发。

拷贝生成的`role-id`、`secret-id`或者`app-token`备用。

### 3.配置运行 Autopcr 

#### Compose (受项目提供Package所限，适用于运行单Web服务模式)

把第二步生成的放在`role-id`、`secret-id`或者`app-token`放到`openbao/secrets`（或者自定义其他路径）目录下。

AppRole 凭据目录需包含 `secret-id`，Role ID 可放在同目录的 `role-id` 文件中，也可通过 `AUTOPCR_OPENBAO_ROLE_ID` 提供。

静态 Token 方式需包含 `app-token` 文件。

在 `openbao/.env` 中设置 `AUTOPCR_OPENBAO_ADDR`和`AUTOPCR_OPENBAO_AUTH_METHOD`
（自定义其他路径还需要设置`AUTOPCR_OPENBAO_AUTH_DIR`），然后启动：

```bash
docker compose --env-file openbao/.env \
  -f openbao/docker-compose.yml \
  -f openbao/docker-compose.manual-bootstrap.yml up -d
```

#### 直接运行

直接运行python，通过环境变量配置时，可使用以下设置。只需按所选认证方式填写对应项目：

| 环境变量 | 用途 | 默认值或示例 |
|---------|------|-------------|
| `AUTOPCR_OPENBAO_ENABLED` | 启用 OpenBao | `false`；启用时设为 `true` |
| `AUTOPCR_OPENBAO_ADDR` | OpenBao API 地址 | `http://127.0.0.1:8200` |
| `AUTOPCR_OPENBAO_AUTH_METHOD` | 认证方式：`approle`、`token` 或 `kubernetes` | `token` |
| `AUTOPCR_OPENBAO_TOKEN_FILE` | 静态 Token 文件；仅 token 模式需要 | `cache/openbao/app-token` |
| `AUTOPCR_OPENBAO_ROLE_ID` | AppRole Role ID，可直接配置 | 空 |
| `AUTOPCR_OPENBAO_ROLE_ID_FILE` | AppRole Role ID 文件；未配置 `ROLE_ID` 时读取 | `cache/openbao/role-id` |
| `AUTOPCR_OPENBAO_SECRET_ID_FILE` | AppRole Secret ID 文件 | `cache/openbao/secret-id` |
| `AUTOPCR_OPENBAO_APPROLE_MOUNT` | AppRole auth mount 名称 | `approle` |

Secret ID 和静态 Token 文件应限制访问权限。静态 Token 不会自动续期，需由管理员负责有效期管理和轮换。

- 单 Web 服务

可用启动参数启用，启动参数优先于环境变量。

```powershell
# AppRole
python3 httpserver_standalone.py `
  --openbao-enabled `
  --openbao-auth-method approle `
  --openbao-addr "https://openbao.example.com:8200" `
  --openbao-role-id "your-role-id" `
  --openbao-secret-id-file ".\openbao\secrets\openbao\secret-id" `
  --openbao-approle-mount approle

# Token
# python3 httpserver_standalone.py `
#   --openbao-enabled `
#   --openbao-auth-method token `
#   --openbao-addr "https://openbao.example.com:8200" `
#   --openbao-token-file "C:\secrets\openbao\app-token"
```

完整选项可运行 `python3 httpserver_standalone.py --help` 查看。

- Hoshino 插件

可通过设配置文件来启用，配置文件设置项优先于环境变量。

使用模板见 [`autopcr.py.example`](./autopcr.py.example)，在 Hoshino 配置目录的 `autopcr.py` 中设置：

```python
AUTOPCR_OPENBAO_ENABLED = True
AUTOPCR_OPENBAO_ADDR = "https://openbao.example.com:8200"
# 使用approle
AUTOPCR_OPENBAO_AUTH_METHOD = "approle"
AUTOPCR_OPENBAO_ROLE_ID = "your-role-id"
AUTOPCR_OPENBAO_SECRET_ID_FILE = "secrets/openbao/secret-id"
# 使用静态token
# AUTOPCR_OPENBAO_AUTH_METHOD = "token"
# AUTOPCR_OPENBAO_TOKEN_FILE = "/path/to/openbao/app-token"
```
**注意:**

`*_FILE` 相对路径以 **Hoshino 进程的当前工作目录** 为基准，不是相对配置文件或插件目录。例如，若 Hoshino 工作目录为 `D:\hoshino`，则 `secrets/app-token` 指向 `D:\hoshino\secrets\app-token`

#### Kubernetes

| `AUTOPCR_OPENBAO_K8S_ROLE` | Kubernetes auth role | 空；Kubernetes 模式必填 |
| `AUTOPCR_OPENBAO_K8S_MOUNT` | Kubernetes auth mount 名称 | `kubernetes` |
| `AUTOPCR_OPENBAO_K8S_JWT_FILE` | Kubernetes ServiceAccount JWT 文件 | `/var/run/secrets/kubernetes.io/serviceaccount/token` |

使用 Kubernetes 认证前，OpenBao 管理员需配置 Kubernetes auth、对应 role 和应用策略。