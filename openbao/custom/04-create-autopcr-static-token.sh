#!/usr/bin/env bash
set -euo pipefail

: "${BAO_ADDR:?Set BAO_ADDR to the external OpenBao URL}"
: "${BAO_TOKEN:?Set BAO_TOKEN to an administrator token allowed to create application tokens}"
: "${AUTOPCR_OPENBAO_TOKEN_FILE:=/run/openbao-app-token}"

TOKEN_FILE="$AUTOPCR_OPENBAO_TOKEN_FILE"
TOKEN_DIR="$(dirname "$TOKEN_FILE")"

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
  echo "The autopcr policy is missing; run 02-setup-autopcr-kv.sh first" >&2
  exit 1
fi

TOKEN_TEMP="$(mktemp "$TOKEN_DIR/.app-token.tmp.XXXXXX")"
trap 'rm -f "$TOKEN_TEMP"' EXIT

bao token create \
  -format=json \
  -policy=autopcr \
  -no-default-policy \
  -orphan \
  -renewable=false \
  -ttl=720h \
  -explicit-max-ttl=720h |
  python3 -c '
import json, sys
token = json.load(sys.stdin)["auth"]["client_token"]
if not token:
    raise SystemExit("OpenBao returned an empty token")
print(token)
' > "$TOKEN_TEMP"

chmod 600 "$TOKEN_TEMP"
mv "$TOKEN_TEMP" "$TOKEN_FILE"
trap - EXIT

unset BAO_TOKEN
printf 'AutoPCR static token saved to %s (expires in 30 days)\n' "$TOKEN_FILE"
