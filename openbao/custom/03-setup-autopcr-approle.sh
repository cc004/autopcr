
#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR:=/run/openbao}"
: "${AUTOPCR_OPENBAO_APP_TOKEN_DIR:=/run/openbao-app}"

umask 077
ADMIN_TOKEN_DIR="$(cd "$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR" && pwd -P)"
APP_TOKEN_DIR="$AUTOPCR_OPENBAO_APP_TOKEN_DIR"
mkdir -p "$APP_TOKEN_DIR"
APP_TOKEN_DIR="$(cd "$APP_TOKEN_DIR" && pwd -P)"

if [[ "$ADMIN_TOKEN_DIR" == "$APP_TOKEN_DIR" ]]; then
  echo "Admin-token and app-token directories must be different" >&2
  exit 1
fi

TOKEN_FILE="$ADMIN_TOKEN_DIR/admin-token"
ROLE_ID_FILE="$APP_TOKEN_DIR/role-id"
SECRET_ID_FILE="$APP_TOKEN_DIR/secret-id"
READY_FILE="$APP_TOKEN_DIR/ready"

if [[ ! -s "$TOKEN_FILE" ]]; then
  echo "Admin token is missing: $TOKEN_FILE" >&2
  exit 1
fi

export BAO_TOKEN
BAO_TOKEN="$(<"$TOKEN_FILE")"

rm -f "$READY_FILE"

# Check whether AppRole authentication is already enabled.
AUTH_METHODS="$(bao auth list -format=json)"

if ! printf '%s' "$AUTH_METHODS" | python3 -c '
import json, sys
methods = json.load(sys.stdin)
method = methods.get("approle/")
if method is None:
    sys.exit(1)
if method.get("type") != "approle":
    raise SystemExit("approle/ exists but is not an AppRole auth method")
'; then
  if ! printf '%s' "$AUTH_METHODS" | python3 -c '
import json, sys
sys.exit(0 if "approle/" in json.load(sys.stdin) else 1)
'; then
    bao auth enable -path=approle approle
  else
    echo "Existing approle/ mount has an incompatible configuration" >&2
    exit 1
  fi
fi

# Create or update the AutoPCR AppRole.
bao write auth/approle/role/autopcr \
  token_policies=autopcr \
  token_no_default_policy=true \
  token_period=720h \
  secret_id_ttl=0 \
  secret_id_num_uses=0

# Retrieve the stable Role ID.
ROLE_ID="$(bao read -field=role_id \
  auth/approle/role/autopcr/role-id)"

if [[ -z "$ROLE_ID" ]]; then
  echo "OpenBao returned an empty Role ID" >&2
  exit 1
fi

# Preserve an existing Secret ID to avoid creating multiple
# indefinitely valid credentials on repeated executions.
if [[ ! -s "$SECRET_ID_FILE" ]]; then
  SECRET_ID="$(bao write -f -field=secret_id \
    auth/approle/role/autopcr/secret-id)"

  if [[ -z "$SECRET_ID" ]]; then
    echo "OpenBao returned an empty Secret ID" >&2
    exit 1
  fi

  SECRET_TEMP="$(mktemp "$APP_TOKEN_DIR/secret-id.tmp.XXXXXX")"
  trap 'rm -f "$SECRET_TEMP"' EXIT

  printf '%s' "$SECRET_ID" > "$SECRET_TEMP"
  chmod 600 "$SECRET_TEMP"
  mv "$SECRET_TEMP" "$SECRET_ID_FILE"
fi

# Save Role ID.
ROLE_TEMP="$(mktemp "$APP_TOKEN_DIR/role-id.tmp.XXXXXX")"
trap 'rm -f "$ROLE_TEMP"' EXIT

printf '%s' "$ROLE_ID" > "$ROLE_TEMP"
chmod 600 "$ROLE_TEMP"
mv "$ROLE_TEMP" "$ROLE_ID_FILE"

# Mark AppRole credentials as ready in the app-token directory.
: > "$READY_FILE"
chmod 600 "$READY_FILE"

unset BAO_TOKEN

printf 'AutoPCR AppRole credentials saved to %s\n' "$APP_TOKEN_DIR"
