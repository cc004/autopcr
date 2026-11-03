
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${BAO_TOKEN:?Use the initial root token only for admin-token creation}"

TOKEN_DIR="${AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR:-/run/openbao/admin}"
TOKEN_FILE="$TOKEN_DIR/admin-token"
READY_FILE="$TOKEN_DIR/ready"

umask 077
mkdir -p "$TOKEN_DIR"

if [[ -s "$TOKEN_FILE" ]]; then
  echo "Admin token already exists: $TOKEN_FILE" >&2
  echo "Refusing to create another token or overwrite the existing one." >&2
  exit 1
fi

rm -f "$READY_FILE"

STATUS="$(bao status -format=json || true)"

if ! printf '%s' "$STATUS" | python3 -c '
import json, sys
status = json.load(sys.stdin)
sys.exit(0 if status.get("initialized") is True
         and status.get("sealed") is False else 1)
'; then
  echo "OpenBao must already be initialized and unsealed" >&2
  exit 1
fi

POLICY_FILE="$(mktemp)"
TOKEN_TEMP="$(mktemp "$TOKEN_DIR/admin-token.tmp.XXXXXX")"

trap 'rm -f "$POLICY_FILE" "$TOKEN_TEMP"' EXIT

cat > "$POLICY_FILE" <<'HCL'
# Inspect existing secrets engines and create the AutoPCR KV mount.
path "sys/mounts" {
  capabilities = ["read", "sudo"]
}

path "sys/mounts/autopcr" {
  capabilities = ["create", "update", "sudo"]
}

# Create or update the AutoPCR application policy.
path "sys/policies/acl/autopcr" {
  capabilities = ["create", "update", "sudo"]
}

# Inspect and enable AppRole authentication.
path "sys/auth" {
  capabilities = ["read", "sudo"]
}

path "sys/auth/approle" {
  capabilities = ["create", "update", "sudo"]
}

# Configure the AutoPCR AppRole and issue its credentials.
path "auth/approle/role/autopcr" {
  capabilities = ["create", "update"]
}

path "auth/approle/role/autopcr/role-id" {
  capabilities = ["read"]
}

path "auth/approle/role/autopcr/secret-id" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup" {
  capabilities = ["update"]
}

path "auth/token/revoke" {
  capabilities = ["update"]
}
HCL

bao policy write autopcr-bootstrap "$POLICY_FILE"

bao token create \
  -format=json \
  -policy=autopcr-bootstrap \
  -no-default-policy \
  -orphan |
  python3 -c '
import json, sys
print(json.load(sys.stdin)["auth"]["client_token"])
' > "$TOKEN_TEMP"

chmod 600 "$TOKEN_TEMP"
mv "$TOKEN_TEMP" "$TOKEN_FILE"

: > "$READY_FILE"
chmod 600 "$READY_FILE"

unset BAO_TOKEN

printf 'Admin token and readiness marker created in %s\n' "$TOKEN_DIR"
