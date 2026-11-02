# 使用外部自定义 OpenBao

使用外部 OpenBao 时，初始化、解封和密钥托管由 OpenBao 服务端负责。手动配置时需启用 KV v2 的 `autopcr/` 引擎并配置受限身份；使用 `docker-compose.auto-bootstrap` 时，这些 KV、策略和 AppRole 配置由 bootstrap 自动创建。支持静态 token 文件、AppRole 和 Kubernetes auth。

## 1. OpenBao init

如果 OpenBao 集群尚未初始化，先在 OpenBao 服务器上设置 `BAO_ADDR`，使 `bao` CLI 指向该集群。

```bash
export BAO_ADDR="https://openbao.example.com:8200"
```

然后执行一次初始化。以下命令使用 Shamir seal，生成 5 份 unseal key、阈值为 3，并将包含 `root_token` 和 unseal keys 的完整 JSON 保存到本地文件；不要对已初始化的集群再次执行：

```bash
umask 077
bao operator init -key-shares=5 -key-threshold=3 -format=json > /tmp/openbao-init-result.json
```

**请立即将 `openbao-init-result.json` 加密备份到其他安全位置**（例如离线介质或密码管理器），并验证备份可读取。文件包含 root token 和解封密钥，必须限制访问权限，切勿提交到代码仓库或长期留在普通服务器目录中。

`operator init` 初始化完成后，使用 Shamir seal 的 OpenBao 仍处于封存状态，因此首次初始化后必须立即解封一次。解封后，OpenBao 会保持解封，直到服务重启、被管理员手动封存，或存储层遇到不可恢复错误；正常运行期间不需要重复执行解封命令。

使用 `openbao-init-result.json` 中任意 **3 份不同的** `unseal_keys_b64` 解封。每次执行命令后，在交互提示中输入一份 key；不要把 key 直接写在命令参数或 shell 历史中：

```sh
bao operator unseal
# 按提示输入第 1 份 unseal key
bao operator unseal
# 按提示输入第 2 份不同的 unseal key
bao operator unseal
# 按提示输入第 3 份不同的 unseal key
bao status
```

确认 `bao status` 显示 `Sealed` 为 `false` 后，OpenBao 即已解封。每次 OpenBao 重启或被重新封存后，都需要重新提交任意 3 份不同的 unseal key。

解封成功后，从初始化结果中读取 root token 并设置 `BAO_TOKEN`，供后续配置命令使用。不要把 token 明文直接粘贴到命令行：

```bash
export BAO_TOKEN="$(sed -n 's/.*"root_token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' /tmp/openbao-init-result.json)"
```

不要将 root token 交给 AutoPCR 或 Compose。使用仓库脚本 [`01-create-admin-token.sh`](./openbao/custom/01-create-admin-token.sh)创建专用的受限 `admin_token`。

运行脚本的管理机器需安装 OpenBao CLI（`bao`）和 Python 3，并能连接已初始化且已解封的 OpenBao。设置 `BAO_ADDR`、`BAO_TOKEN`（初始 root token）和 `AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR` 后运行脚本。脚本会检查 OpenBao 状态并在该目录生成 `admin-token` 和 `ready`；`ready` 表示 admin token 已生成，供自动 bootstrap 检查。脚本不会覆盖已有的 admin token。

**Openbao初始化后，autopcr的bootstrap可以按需采用自动或者手动的方式**



## 2. OpenBao bootstrap

完成上面的初始化后，以下方式二选一执行以下步骤来完成OpenBao的bootstrap。

### (a)自动bootstrap并自提供凭据 

只需运行 [`01-create-admin-token.sh`](./openbao/custom/01-create-admin-token.sh)。该脚本生成 `admin-token` 和 `ready`；`ready` 表示 admin token 已准备好，Compose bootstrap 会检查该标记。 bootstrap 容器会自行配置 KV、策略和 AppRole。管理员 token 目录只挂载给该容器；AutoPCR 本身只获得 bootstrap 写入 Docker 命名卷的 AppRole 凭据。妥善保护该目录，并确保 token 在 bootstrap 需要运行时仍有效。

### (b)手动bootstrap并手动取得凭据

#### 1.手动 bootstrap

先按上文运行 [`01-create-admin-token.sh`](./openbao/custom/01-create-admin-token.sh) 创建 `admin-token` 和 admin token 的 `ready` 标记，然后运行 [`02-setup-autopcr-kv.sh`](./openbao/custom/02-setup-autopcr-kv.sh) 创建或校验 `autopcr/` KV v2 mount 并配置应用策略。它从 `AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/admin-token` 读取受限 admin token，不需要再设置 root token。

#### 2.从 OpenBao 取得凭据

完成上面的手动bootstrap后，按认证方式**二选一**执行以下步骤，取得 AutoPCR 连接 OpenBao 所需凭据。

##### AppRole 方式（推荐用于服务部署）

AppRole 使用 Role ID 和 Secret ID 登录，AutoPCR 自动缓存并续租周期 token。运行 [`03-setup-autopcr-approle.sh`](./openbao/custom/03-setup-autopcr-approle.sh) 启用/校验默认的 `approle` mount、配置角色并取得应用凭据。设置 `AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR` 指向含 `admin-token` 的目录，并将 `AUTOPCR_OPENBAO_APP_TOKEN_DIR` 指向独立的应用凭据目录。脚本从前者读取 admin token，把 Role ID、Secret ID 和 `ready` 写入后者。admin 目录的 `ready` 由第一步创建，表示 admin token 已生成；app 目录的 `ready` 由第三步创建，表示 AppRole 凭据已准备好。Secret ID 不过期，应妥善保护并由管理员按需轮换。

将 `AUTOPCR_OPENBAO_APP_TOKEN_DIR` 设为手动 Compose 的 `AUTOPCR_OPENBAO_AUTH_DIR`，这样 `role-id` 和 `secret-id` 可直接供 AutoPCR 使用。不要把包含 `admin-token` 的目录挂载给 AutoPCR。Role ID 本身不是密码；Secret ID 是密码，应妥善保管。初始化管理员 token 不需要、也不应提供给 AutoPCR。

**凭据备份提醒：** OpenBao 不会再次显示已生成的静态 Token 或 Secret ID。请把 AutoPCR 实际使用的凭据文件纳入安全备份；丢失时需由管理员重新生成凭据并更新 AutoPCR 配置。切勿将 token、Secret ID 或管理员 token 上传到代码仓库。

##### 静态 Token 方式（设置简单，但需要频繁轮转）

静态 Token 仅从文件读取，AutoPCR 不会自动续期。[`04-create-autopcr-static-token.sh`](./openbao/custom/04-create-autopcr-static-token.sh)。该脚本使用 `BAO_TOKEN` 中的 root token 创建仅附加 `autopcr` 策略、有效期为 30 天且不可续期的 token，并以仅当前用户可读的权限写入 `AUTOPCR_OPENBAO_TOKEN_FILE` 指定的文件。只在管理端使用 root token，不要把它提供给 AutoPCR；脚本不会覆盖已有 token 文件。

配置 AutoPCR 使用 `AUTOPCR_OPENBAO_AUTH_METHOD=token`，并将 `AUTOPCR_OPENBAO_TOKEN_FILE` 指向生成的文件。Token 文件是敏感凭据；到期或怀疑泄露时，由管理员撤销旧 token、重新签发并替换文件。