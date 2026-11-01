
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR:=/run/openbao}"

TOKEN_FILE="$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/admin-token"

if [[ ! -s "$TOKEN_FILE" ]]; then
  echo "Admin token is missing: $TOKEN_FILE" >&2
  exit 1
fi

export BAO_TOKEN
BAO_TOKEN="$(<"$TOKEN_FILE")"

# Check whether the autopcr mount already exists.
MOUNTS="$(bao secrets list -format=json)"

if ! printf '%s' "$MOUNTS" | python3 -c '
import json, sys
mounts = json.load(sys.stdin)
mount = mounts.get("autopcr/")
if mount is None:
    sys.exit(1)
if mount.get("type") != "kv" or mount.get("options", {}).get("version") != "2":
    raise SystemExit("Existing autopcr/ mount is not KV v2")
'; then
  # Create the mount only when it does not exist.
  if ! printf '%s' "$MOUNTS" | python3 -c '
import json, sys
sys.exit(0 if "autopcr/" in json.load(sys.stdin) else 1)
'; then
    bao secrets enable -path=autopcr kv-v2
  else
    echo "Existing autopcr/ mount has an incompatible configuration" >&2
    exit 1
  fi
fi

POLICY_FILE="$(mktemp)"
trap 'rm -f "$POLICY_FILE"' EXIT

cat > "$POLICY_FILE" <<'HCL'
path "autopcr/data/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "autopcr/metadata/*" {
  capabilities = ["list", "read", "delete"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}
HCL

bao policy write autopcr "$POLICY_FILE"

printf 'AutoPCR KV v2 mount and policy configured\n'
