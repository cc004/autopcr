#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR:=/run/openbao/admin}"
: "${AUTOPCR_OPENBAO_TOKEN_FILE:=/run/openbao/app/app-token}"

ADMIN_TOKEN_FILE="$AUTOPCR_OPENBAO_ADMIN_TOKEN_DIR/admin-token"
TOKEN_FILE="$AUTOPCR_OPENBAO_TOKEN_FILE"
TOKEN_DIR="$(dirname "$TOKEN_FILE")"

if [[ ! -s "$ADMIN_TOKEN_FILE" ]]; then
  echo "Admin token is missing: $ADMIN_TOKEN_FILE" >&2
  exit 1
fi

export BAO_TOKEN
BAO_TOKEN="$(<"$ADMIN_TOKEN_FILE")"

umask 077
mkdir -p "$TOKEN_DIR"

if [[ -e "$TOKEN_FILE" ]]; then
  echo "Token file already exists: $TOKEN_FILE" >&2
  echo "Refusing to overwrite it. Remove it only after arranging safe token rotation." >&2
  exit 1
fi

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

if ! bao policy read autopcr >/dev/null; then
  echo "Cannot read the autopcr policy; ensure the admin token has read access to sys/policies/acl/autopcr." >&2
  echo "If the policy is missing, run 02-setup-autopcr-kv.sh first." >&2
  exit 1
fi

TOKEN_TEMP="$(mktemp "$TOKEN_DIR/.app-token.tmp.XXXXXX")"
TOKEN_ERROR="$(mktemp "$TOKEN_DIR/.app-token.error.XXXXXX")"
trap 'rm -f "$TOKEN_TEMP" "$TOKEN_ERROR"' EXIT

if ! TOKEN_RESPONSE="$(bao token create \
  -format=json \
  -policy=autopcr \
  -no-default-policy \
  -orphan \
  -renewable=false \
  -ttl=720h \
  -explicit-max-ttl=720h 2>"$TOKEN_ERROR")"; then
  cat "$TOKEN_ERROR" >&2
  echo "Failed to create the AutoPCR token; the admin policy needs update and sudo access to auth/token/create-orphan." >&2
  exit 1
fi

if ! printf '%s' "$TOKEN_RESPONSE" | python3 -c '
import json, sys

try:
    token = json.load(sys.stdin)["auth"]["client_token"]
except (KeyError, json.JSONDecodeError, TypeError) as error:
    raise SystemExit("OpenBao returned an invalid token creation response") from error
if not isinstance(token, str) or not token:
    raise SystemExit("OpenBao returned an empty token")
print(token)
' > "$TOKEN_TEMP"; then
  exit 1
fi

chmod 600 "$TOKEN_TEMP"
mv "$TOKEN_TEMP" "$TOKEN_FILE"
rm -f "$TOKEN_ERROR"
trap - EXIT

unset BAO_TOKEN
printf 'AutoPCR static token saved to %s (expires in 30 days)\n' "$TOKEN_FILE"
