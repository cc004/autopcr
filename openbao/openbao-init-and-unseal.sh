#!/bin/sh
set -eu

KEY_DIR="${AUTOPCR_OPENBAO_KEY_DIR:-/openbao/keys}"
BOOTSTRAP_DIR="${AUTOPCR_OPENBAO_BOOTSTRAP_DIR:-/vault-bootstrap}"
ROOT_TOKEN_FILE="$KEY_DIR/root-token"
RECOVERY_FILE="$KEY_DIR/recovery.json"
ROOT_TOKEN_HANDOFF="$BOOTSTRAP_DIR/root-token"
READY_FILE="$BOOTSTRAP_DIR/ready"
KEY_SHARES=5
KEY_THRESHOLD=3

umask 077
mkdir -p "$KEY_DIR" "$BOOTSTRAP_DIR"
rm -f "$READY_FILE"

write_secret() {
    destination="$1"
    value="$2"
    temporary="$destination.tmp"
    printf '%s' "$value" > "$temporary"
    chmod 600 "$temporary"
    mv -f "$temporary" "$destination"
}

json_field() {
    field="$1"
    file="$2"
    tr -d '\n' < "$file" \
        | sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p"
}

json_number() {
    field="$1"
    file="$2"
    tr -d '\n' < "$file" \
        | sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\\([0-9][0-9]*\\).*/\\1/p"
}

json_unseal_keys() {
    file="$1"
    tr -d '\n' < "$file" \
        | sed -n 's/.*"unseal_keys_b64"[[:space:]]*:[[:space:]]*\[\([^]]*\)\].*/\1/p' \
        | tr ',' '\n' \
        | sed -n 's/^[[:space:]]*"\([^"]*\)".*/\1/p'
}

current_sealed() {
    bao status -format=json 2>/dev/null \
        | tr -d '\n' \
        | sed -n 's/.*"sealed"[[:space:]]*:[[:space:]]*\(true\|false\).*/\1/p'
}

recover_key_material() {
    if [ ! -s "$RECOVERY_FILE" ]; then
        return 1
    fi
    shares="$(json_number unseal_shares "$RECOVERY_FILE")"
    threshold="$(json_number unseal_threshold "$RECOVERY_FILE")"
    key_count="$(json_unseal_keys "$RECOVERY_FILE" | grep -c . || true)"
    root_token="$(json_field root_token "$RECOVERY_FILE")"
    if [ "$shares" != "$KEY_SHARES" ] \
        || [ "$threshold" != "$KEY_THRESHOLD" ] \
        || [ "$key_count" -ne "$KEY_SHARES" ] \
        || [ -z "$root_token" ]; then
        echo "Stored OpenBao recovery file is invalid or does not contain a 3-of-5 key set"
        return 1
    fi
    if [ ! -s "$ROOT_TOKEN_FILE" ]; then
        write_secret "$ROOT_TOKEN_FILE" "$root_token" || return 1
    fi
}

apply_unseal_shares() {
    if [ ! -s "$RECOVERY_FILE" ]; then
        echo "OpenBao recovery file is missing; cannot unseal"
        return 1
    fi
    applied=0
    for key in $(json_unseal_keys "$RECOVERY_FILE"); do
        if [ "$(current_sealed || true)" = "false" ]; then
            break
        fi
        applied=$((applied + 1))
        echo "OpenBao unsealing with share $applied/$KEY_THRESHOLD"
        error_file="$(mktemp)"
        result=0
        bao operator unseal "$key" >/dev/null 2>"$error_file" || result=$?
        error="$(cat "$error_file")"
        rm -f "$error_file"
        if [ "$result" -ne 0 ]; then
            if [ "$(current_sealed || true)" = "false" ]; then
                break
            fi
            echo "OpenBao rejected unseal share $applied: ${error:-no error details}"
        fi
    done
    if [ "$(current_sealed || true)" != "false" ]; then
        echo "OpenBao remains sealed after applying $applied share(s); threshold is $KEY_THRESHOLD"
        return 1
    fi
    echo "OpenBao unsealed with $KEY_THRESHOLD-of-$KEY_SHARES shares"
}

while true; do
    status="$(bao status -format=json 2>/dev/null || true)"

    if [ -z "$status" ]; then
        rm -f "$READY_FILE"
        echo "OpenBao is unreachable; retrying init/unseal check"
    else
        if printf '%s' "$status" | grep -Eq '"initialized"[[:space:]]*:[[:space:]]*false'; then
            rm -f "$READY_FILE"
            if [ -s "$RECOVERY_FILE" ] \
                || [ -s "$ROOT_TOKEN_FILE" ]; then
                echo "OpenBao storage is uninitialized but saved key material exists."
                echo "Refusing to initialize a new cluster; restore the matching Raft data volume."
                exit 1
            fi
            init_temporary="$RECOVERY_FILE.tmp"
            if bao operator init \
                -key-shares="$KEY_SHARES" \
                -key-threshold="$KEY_THRESHOLD" \
                -format=json \
                > "$init_temporary" 2>/dev/null; then
                chmod 600 "$init_temporary"
                mv -f "$init_temporary" "$RECOVERY_FILE"
                if recover_key_material; then
                    echo "OpenBao initialized with $KEY_THRESHOLD-of-$KEY_SHARES Shamir shares; recovery file saved"
                    status="$(bao status -format=json 2>/dev/null || true)"
                fi
            else
                rm -f "$init_temporary"
                echo "OpenBao initialization failed or returned incomplete key material"
            fi
        fi

        if printf '%s' "$status" | grep -Eq '"initialized"[[:space:]]*:[[:space:]]*true' \
            && [ ! -s "$ROOT_TOKEN_FILE" ]; then
            if ! recover_key_material; then
                echo "OpenBao is initialized but key material could not be recovered"
            fi
        fi

        if printf '%s' "$status" | grep -Eq '"sealed"[[:space:]]*:[[:space:]]*true'; then
            if ! apply_unseal_shares; then
                echo "OpenBao unseal failed; retrying"
            fi
        fi

        status="$(bao status -format=json 2>/dev/null || true)"
        if [ -n "$status" ] \
            && printf '%s' "$status" | grep -Eq '"sealed"[[:space:]]*:[[:space:]]*false' \
            && [ -s "$ROOT_TOKEN_FILE" ]; then
            root_token="$(cat "$ROOT_TOKEN_FILE")"
            write_secret "$ROOT_TOKEN_HANDOFF" "$root_token"
            : > "$READY_FILE"
            chmod 600 "$READY_FILE"
        else
            rm -f "$READY_FILE"
        fi
    fi

    sleep 30
done
