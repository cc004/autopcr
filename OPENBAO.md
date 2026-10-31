# 使用外部自定义 OpenBao

使用外部 OpenBao 时，初始化、解封和密钥托管由 OpenBao 服务端负责。服务需启用 KV v2 的 `autopcr/` 引擎，并为 AutoPCR 配置受限身份（`autopcr/data/*` 具备 create/read/update/delete，`autopcr/metadata/*` 具备 read/delete；AppRole/Kubernetes 登录 token 需要 `auth/token/renew-self` 的 update 权限）。支持静态 token 文件、AppRole 和 Kubernetes auth。

## OpenBao 初始化

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

首次初始化后，或上述情况导致 OpenBao 再次封存时，使用 `openbao-init-result.json` 中任意 **3 份不同的** `unseal_keys_b64` 解封。每次执行命令后，在交互提示中输入一份 key；不要把 key 直接写在命令参数或 shell 历史中：

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

执行后续配置命令的机器需安装 `bao` CLI，并已设置指向 OpenBao 的 `BAO_ADDR` 及管理员身份 `BAO_TOKEN`。管理员身份只用于初始化和获取凭据，绝不填入 AutoPCR 配置。以下步骤分为共同的 OpenBao 初始化和任选一种凭据取得方法；相关 `autopcr/` 路径及认证配置应为新建，重复执行 enable 命令会报“已存在”。

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

## OpenBao 凭据取得

完成上面的共同初始化后，按认证方式**二选一**执行以下步骤，取得 AutoPCR 连接 OpenBao 所需凭据。

### AppRole（推荐用于服务部署）

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

### 静态 Token（设置简单，但需要频繁轮转）

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
