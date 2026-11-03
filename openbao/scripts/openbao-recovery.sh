#!/bin/sh
set -eu
umask 077

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-$(basename "$PROJECT_DIR")}"
DATA_VOLUME="${PROJECT_NAME}_autopcr_openbao_data"
KEYS_VOLUME="${PROJECT_NAME}_autopcr_openbao_keys"
BOOTSTRAP_VOLUME="${PROJECT_NAME}_autopcr_openbao_bootstrap"
BACKUP_DIR=""
RUNNING_SERVICES=""

usage() {
    cat >&2 <<EOF
Usage:
  $0 export <recovery-file>
  $0 backup <directory>
  $0 restore <directory> [--force]

The exported recovery file contains unseal material and the initial root token.
Backups contain the Raft data volume and matching initialization keys.
Treat both as secrets and store them encrypted off-host.
EOF
    exit 2
}

log() {
    printf '[openbao-recovery] %s\n' "$*" >&2
}

die() {
    log "ERROR: $*"
    exit 1
}

require_docker() {
    command -v docker >/dev/null 2>&1 || die "docker not found in PATH"
    docker compose version >/dev/null 2>&1 || die "Docker Compose v2 is required"
}

volume_exists() {
    docker volume inspect "$1" >/dev/null 2>&1
}

create_volume() {
    volume="$1"
    compose_volume="$2"
    if ! volume_exists "$volume"; then
        docker volume create \
            --label "com.docker.compose.project=$PROJECT_NAME" \
            --label "com.docker.compose.volume=$compose_volume" \
            "$volume" >/dev/null
    fi
}

volume_has_data() {
    docker run --rm \
        -v "$1:/volume:ro" \
        alpine:3.20 \
        sh -c 'test -n "$(ls -A /volume)"'
}

export_recovery() {
    [ "$#" -eq 1 ] || usage
    output="$1"
    [ -n "$output" ] || usage
    volume_exists "$KEYS_VOLUME" || die "initialization keys volume not found: $KEYS_VOLUME"

    if [ "$output" = "-" ]; then
        docker run --rm \
            -v "$KEYS_VOLUME:/keys:ro" \
            alpine:3.20 \
            sh -eu -c '
                if [ -s /keys/recovery.json ]; then
                    cat /keys/recovery.json
                else
                    echo "OpenBao recovery file not found; has initialization completed?" >&2
                    exit 1
                fi
            '
        return
    fi

    [ ! -e "$output" ] || die "refusing to overwrite existing file: $output"
    output_dir="$(dirname -- "$output")"
    output_name="$(basename -- "$output")"
    mkdir -p "$output_dir"
    output_dir="$(CDPATH= cd -- "$output_dir" && pwd)"
    temporary="$(mktemp "$output_dir/.$output_name.tmp.XXXXXX")"
    if ! docker run --rm \
        -v "$KEYS_VOLUME:/keys:ro" \
        alpine:3.20 \
        sh -eu -c '
            if [ -s /keys/recovery.json ]; then
                cat /keys/recovery.json
            else
                echo "OpenBao recovery file not found; has initialization completed?" >&2
                exit 1
            fi
        ' > "$temporary"; then
        rm -f "$temporary"
        die "failed to export OpenBao recovery file"
    fi
    chmod 600 "$temporary"
    mv "$temporary" "$output_dir/$output_name"
    log "recovery file exported to $output_dir/$output_name; store it encrypted off-host"
}

restart_services() {
    status=$?
    trap - EXIT HUP INT TERM
    for service in openbao openbao-init openbao-bootstrap autopcr; do
        if printf '%s\n' "$RUNNING_SERVICES" | grep -Fxq "$service"; then
            if ! docker compose start "$service"; then
                log "ERROR: failed to restart previously running service: $service"
                [ "$status" -ne 0 ] || status=1
            fi
        fi
    done
    exit "$status"
}

backup() {
    [ "$#" -eq 1 ] || usage
    [ -n "$1" ] || usage
    BACKUP_DIR="$1"
    mkdir -p "$BACKUP_DIR"
    BACKUP_DIR="$(CDPATH= cd -- "$BACKUP_DIR" && pwd)"
    [ ! -e "$BACKUP_DIR/raft-data.tar.gz" ] || die "backup file already exists: $BACKUP_DIR/raft-data.tar.gz"
    [ ! -e "$BACKUP_DIR/init-keys.tar.gz" ] || die "backup file already exists: $BACKUP_DIR/init-keys.tar.gz"
    volume_exists "$DATA_VOLUME" || die "Raft volume not found: $DATA_VOLUME"
    volume_exists "$KEYS_VOLUME" || die "initialization keys volume not found: $KEYS_VOLUME"

    cd "$PROJECT_DIR"
    RUNNING_SERVICES="$(docker compose ps --services --status running)"
    trap restart_services EXIT
    trap 'exit 129' HUP
    trap 'exit 130' INT
    trap 'exit 143' TERM
    docker compose stop autopcr openbao-bootstrap openbao-init openbao

    log "backing up stopped Raft volume $DATA_VOLUME"
    docker run --rm \
        -v "$DATA_VOLUME:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine:3.20 \
        tar -czpf /backup/raft-data.tar.gz -C /source .

    log "backing up matching initialization keys volume $KEYS_VOLUME"
    docker run --rm \
        -v "$KEYS_VOLUME:/source:ro" \
        alpine:3.20 \
        sh -eu -c '
            test -s /source/recovery.json
            test -s /source/root-token
        '
    docker run --rm \
        -v "$KEYS_VOLUME:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine:3.20 \
        tar -czpf /backup/init-keys.tar.gz -C /source .

    chmod 600 "$BACKUP_DIR/raft-data.tar.gz" "$BACKUP_DIR/init-keys.tar.gz"
    log "backup completed in $BACKUP_DIR"
}

restore_volume() {
    volume="$1"
    compose_volume="$2"
    archive="$3"
    force="$4"

    create_volume "$volume" "$compose_volume"
    if volume_has_data "$volume" && [ "$force" != "true" ]; then
        die "$volume is not empty; use --force to replace it"
    fi

    docker run --rm \
        -v "$volume:/target" \
        -v "$BACKUP_DIR:/backup:ro" \
        alpine:3.20 \
        sh -eu -c '
            if [ "$1" = "true" ]; then
                find /target -mindepth 1 -maxdepth 1 -exec rm -rf {} +
            fi
            tar -xzpf "/backup/$2" -C /target
        ' sh "$force" "$archive"
}

restore() {
    [ "$#" -ge 1 ] || usage
    [ "$#" -le 2 ] || usage
    BACKUP_DIR="$1"
    force=false
    if [ "$#" -eq 2 ]; then
        [ "$2" = "--force" ] || usage
        force=true
    fi
    [ -d "$BACKUP_DIR" ] || die "backup directory does not exist: $BACKUP_DIR"
    BACKUP_DIR="$(CDPATH= cd -- "$BACKUP_DIR" && pwd)"
    [ -s "$BACKUP_DIR/raft-data.tar.gz" ] || die "missing or empty raft-data.tar.gz"
    [ -s "$BACKUP_DIR/init-keys.tar.gz" ] || die "missing or empty init-keys.tar.gz"
    docker run --rm \
        -v "$BACKUP_DIR:/backup:ro" \
        alpine:3.20 \
        sh -eu -c '
            tar -tzf /backup/raft-data.tar.gz >/dev/null
            tar -tzf /backup/init-keys.tar.gz |
                grep -Eq "(^|/)recovery\.json$"
            tar -tzf /backup/init-keys.tar.gz |
                grep -Eq "(^|/)root-token$"
        '

    cd "$PROJECT_DIR"
    running_services="$(docker compose ps --services --status running)"
    [ -z "$running_services" ] || die "stop the Compose stack before restoring volumes"

    log "restoring Raft data and matching initialization keys"
    restore_volume "$DATA_VOLUME" autopcr_openbao_data raft-data.tar.gz "$force"
    restore_volume "$KEYS_VOLUME" autopcr_openbao_keys init-keys.tar.gz "$force"
    docker compose rm -f openbao-bootstrap
    if volume_exists "$BOOTSTRAP_VOLUME"; then
        docker run --rm \
            -v "$BOOTSTRAP_VOLUME:/bootstrap" \
            alpine:3.20 \
            rm -f /bootstrap/ready /bootstrap/root-token
    fi
    log "restore completed; start the stack with: docker compose up -d"
}

require_docker
[ "$#" -ge 1 ] || usage
command="$1"
shift

case "$command" in
    export) export_recovery "$@" ;;
    backup) backup "$@" ;;
    restore) restore "$@" ;;
    -h|--help|help) usage ;;
    *) usage ;;
esac
