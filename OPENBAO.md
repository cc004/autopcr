# 使用外部自定义 OpenBao

使用外部 OpenBao 时，初始化、解封和密钥托管由 OpenBao 服务端负责。手动配置时需启用 KV v2 的 `autopcr/` 引擎并配置受限身份；使用 `docker-compose.auto-bootstrap` 时，这些 KV、策略和 AppRole 配置由 bootstrap 自动创建。支持静态 token 文件、AppRole 和 Kubernetes auth。

## (1)OpenBao 初始化

如果 OpenBao 集群尚未初始化，先在 OpenBao 服务器上设置 `BAO_ADDR`，使 `bao` CLI 指向该集群。此时尚无 root token，因此先不要设置 `BAO_TOKEN`：

```bash
export BAO_ADDR="https://openbao.example.com:8200"
```

然后执行一次初始化。以下命令使用 Shamir seal，生成 5 份 unseal key、阈值为 3，并将包含 `root_token` 和 unseal keys 的完整 JSON 保存到本地文件；不要对已初始化的集群再次执行：

```bash
umask 077
bao operator init -key-shares=5 -key-threshold=3 -format=json > openbao-init-result.json
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
export BAO_TOKEN="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["root_token"])' openbao-init-result.json)"
```

不要直接使用 root token 。先用上一步导出的 root token 创建一个专用、受策略限制的 `admin_token`，之后只读取这个 token。以下策略仅允许 bootstrap 管理 `autopcr/` KV、自己的策略和 AppRole，并检查/撤销它创建的 AppRole 登录 token；默认 AppRole mount 为 `approle`。如果设置了自定义 `AUTOPCR_OPENBAO_APPROLE_MOUNT`，需同步替换策略中的 `sys/auth/approle` 和 `auth/approle/` 路径。

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${BAO_TOKEN:?Use the initial root token only to create this restricted token}"
: "${AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR:?Set a secure directory for the admin-token file}"

umask 077
mkdir -p "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR"
rm -f "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/ready"
STATUS="$(bao status -format=json || true)"
if ! printf '%s' "$STATUS" | python3 -c '
import json, sys
status = json.load(sys.stdin)
sys.exit(0 if status.get("initialized") is True and status.get("sealed") is False else 1)
'; then
  echo "OpenBao must already be initialized and unsealed" >&2
  exit 1
fi

POLICY_FILE="$(mktemp)"
TOKEN_TEMP="$(mktemp "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/admin-token.tmp.XXXXXX")"
trap 'rm -f "$POLICY_FILE" "$TOKEN_TEMP"' EXIT

cat > "$POLICY_FILE" <<'HCL'
path "sys/mounts" {
  capabilities = ["read", "sudo"]
}

path "sys/mounts/autopcr" {
  capabilities = ["create", "update", "sudo"]
}

path "sys/policies/acl/autopcr" {
  capabilities = ["create", "update", "sudo"]
}

path "sys/auth" {
  capabilities = ["read", "sudo"]
}

path "sys/auth/approle" {
  capabilities = ["create", "update", "sudo"]
}

path "auth/approle/role/autopcr" {
  capabilities = ["create", "update"]
}

path "auth/approle/role/autopcr/role-id" {
  capabilities = ["read"]
}

path "auth/approle/role/autopcr/secret-id" {
  capabilities = ["update"]
}

path "auth/token/lookup" {
  capabilities = ["update", "sudo"]
}

path "auth/token/revoke" {
  capabilities = ["update", "sudo"]
}
HCL

bao policy write autopcr-bootstrap "$POLICY_FILE"
bao token create -format=json -policy=autopcr-bootstrap -no-default-policy -orphan |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["auth"]["client_token"])' \
  > "$TOKEN_TEMP"
chmod 600 "$TOKEN_TEMP"
mv "$TOKEN_TEMP" "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/admin-token"
: > "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/ready"
chmod 600 "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/ready"
unset BAO_TOKEN
printf 'Restricted admin_token and OpenBao readiness marker saved to %s\n' "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR"
```

**Openbao初始化后，autopcr的bootstrap可以按需采用自动或者手动的方式**

## (2)(a)自动bootstrap并自提供凭据 

将 `AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR` 指向包含 `admin-token` 和 `ready` 的目录提供给外部 Compose 配置。上面的 shell 会先验证 OpenBao 已初始化且未封存，成功创建 token 后才写入 `ready`；Compose bootstrap 以该文件作为启动前置检查。管理员 token 目录只挂载给一次性 bootstrap 容器，AutoPCR 本身只获得 bootstrap 创建的 AppRole 凭据。妥善保护该目录，并确保 token 在 bootstrap 需要运行时仍有效；如 token 过期，重新签发后再运行 bootstrap。

## (2)(b)手动bootstrap并手动取得凭据

### 手动 bootstrap

执行命令的机器需安装 `bao` CLI，并已设置指向 OpenBao 的 `BAO_ADDR` 及管理员身份 `BAO_TOKEN`。管理员身份只用于初始化和获取凭据，绝不填入 AutoPCR 配置。以下步骤分为共同的 OpenBao 初始化和任选一种凭据取得方法；相关 `autopcr/` 路径及认证配置应为新建，重复执行 enable 命令会报“已存在”。

以下共同步骤启用 AutoPCR 专用 KV v2 引擎并创建基础最小权限策略。AppRole 所需的 token 自续租权限会在对应的凭据取得步骤中追加。

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${BAO_TOKEN:?Authenticate bao CLI with an administrator token}"

POLICY_FILE="$(mktemp)"
trap 'rm -f "$POLICY_FILE"' EXIT

cat > "$POLICY_FILE" <<'HCL'
path "autopcr/data/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "autopcr/metadata/*" {
  capabilities = ["read", "delete"]
}
HCL

bao secrets enable -path=autopcr kv-v2
bao policy write autopcr "$POLICY_FILE"
```

### 手动 OpenBao 取得凭据

完成上面的手动bootstrap后，按认证方式**二选一**执行以下步骤，取得 AutoPCR 连接 OpenBao 所需凭据。

#### (a)AppRole（推荐用于服务部署）

AppRole 使用 Role ID 和 Secret ID 登录，AutoPCR 自动缓存并续租周期 token。Secret ID 保存在文件中；本步骤生成的 Secret ID 不过期，需妥善保护并由管理员按需轮换。

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${BAO_TOKEN:?Authenticate bao CLI with an administrator token}"
: "${AUTOPCR_OPENBAO_SECRET_ID_FILE:?Set a secure path for the generated Secret ID}"

APPROLE_MOUNT="${AUTOPCR_OPENBAO_APPROLE_MOUNT:-approle}"
APPROLE_MOUNT="${APPROLE_MOUNT#/}"
APPROLE_MOUNT="${APPROLE_MOUNT%/}"
umask 077
mkdir -p "$(dirname "$AUTOPCR_OPENBAO_SECRET_ID_FILE")"
POLICY_FILE="$(mktemp)"
SECRET_ID_TEMP="$(mktemp "${AUTOPCR_OPENBAO_SECRET_ID_FILE}.tmp.XXXXXX")"
trap 'rm -f "$POLICY_FILE" "$SECRET_ID_TEMP"' EXIT

cat > "$POLICY_FILE" <<'HCL'
path "autopcr/data/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "autopcr/metadata/*" {
  capabilities = ["read", "delete"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
HCL

bao auth enable -path="$APPROLE_MOUNT" approle
bao policy write autopcr "$POLICY_FILE"
bao write "auth/$APPROLE_MOUNT/role/autopcr" \
  token_policies=autopcr \
  token_no_default_policy=true \
  token_period=720h \
  secret_id_ttl=0 \
  secret_id_num_uses=0

ROLE_ID="$(bao read -field=role_id "auth/$APPROLE_MOUNT/role/autopcr/role-id")"
bao write -format=json -f "auth/$APPROLE_MOUNT/role/autopcr/secret-id" |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["data"]["secret_id"])' \
  > "$SECRET_ID_TEMP"
chmod 600 "$SECRET_ID_TEMP"
mv "$SECRET_ID_TEMP" "$AUTOPCR_OPENBAO_SECRET_ID_FILE"

printf 'Role ID: %s\n' "$ROLE_ID"
printf 'Secret ID saved to: %s\n' "$AUTOPCR_OPENBAO_SECRET_ID_FILE"
```

AutoPCR 配置正确的 `AUTOPCR_OPENBAO_ADDR`、`AUTOPCR_OPENBAO_AUTH_METHOD=approle`、脚本输出的 Role ID、Secret ID 文件路径，以及相同的 `AUTOPCR_OPENBAO_APPROLE_MOUNT`。Role ID 本身不是密码；Secret ID 是密码，应妥善保管。初始化管理员 token 不需要、也不应提供给 AutoPCR。

**凭据备份提醒：** OpenBao 不会再次显示已生成的静态 Token 或 Secret ID。请把 AutoPCR 实际使用的凭据文件纳入安全备份；丢失时需由管理员重新生成凭据并更新 AutoPCR 配置。切勿将 token、Secret ID 或管理员 token 上传到代码仓库。

#### (b)静态 Token（设置简单，但需要频繁轮转）

静态 Token 仅从文件读取，AutoPCR 不会自动续期。以下步骤创建一个只允许访问 AutoPCR 密钥、有效期为 30 天且不可续期的 token，并将其安全写入文件；token 到期前需由管理员生成新 token 并替换文件。

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${AUTOPCR_OPENBAO_TOKEN_FILE:?Set a secure path for the generated token}"

umask 077
mkdir -p "$(dirname "$AUTOPCR_OPENBAO_TOKEN_FILE")"
TOKEN_TEMP="$(mktemp "${AUTOPCR_OPENBAO_TOKEN_FILE}.tmp.XXXXXX")"
trap 'rm -f "$TOKEN_TEMP"' EXIT

bao write -format=json auth/token/create \
  policies=autopcr \
  no_default_policy=true \
  ttl=720h \
  renewable=false |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["auth"]["client_token"])' \
  > "$TOKEN_TEMP"
chmod 600 "$TOKEN_TEMP"
mv "$TOKEN_TEMP" "$AUTOPCR_OPENBAO_TOKEN_FILE"

printf 'Token saved to: %s\n' "$AUTOPCR_OPENBAO_TOKEN_FILE"
```

AutoPCR 配置正确的 `AUTOPCR_OPENBAO_ADDR`、`AUTOPCR_OPENBAO_AUTH_METHOD=token`，将 `AUTOPCR_OPENBAO_TOKEN_FILE` 指向脚本生成的文件。Token 文件是敏感凭据，要限制读取权限；Token 到期或怀疑泄露时，由管理员生成新 token 并替换文件，必要时撤销旧 token。