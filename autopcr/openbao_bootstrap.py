import logging
import os
from pathlib import Path

import requests


ADDRESS = os.getenv("AUTOPCR_OPENBAO_ADDR", "http://openbao:8200").rstrip("/")
APP_DIR = Path(os.getenv("AUTOPCR_OPENBAO_TOKEN_DIR", "/run/openbao"))
INIT_READY_FILE = Path(os.getenv("AUTOPCR_OPENBAO_INIT_READY_FILE", "/vault-bootstrap/ready"))
BOOTSTRAP_TOKEN_FILE = Path(
    os.getenv("AUTOPCR_OPENBAO_BOOTSTRAP_TOKEN_FILE", "/vault-bootstrap/root-token")
)
APPROLE_ROLE_ID_FILE = APP_DIR / "role-id"
APPROLE_SECRET_ID_FILE = APP_DIR / "secret-id"
READY_FILE = APP_DIR / "ready"
APPROLE_TOKEN_PERIOD = "720h"
APPROLE_MOUNT = os.getenv("AUTOPCR_OPENBAO_APPROLE_MOUNT", "approle").strip("/")
APPROLE_NAME = "autopcr"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("openbao-bootstrap")


def atomic_write(path: Path, value: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w") as output:
        output.write(value)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)
    os.chmod(path, 0o600)


def api(method: str, path: str, token=None, payload=None):
    headers = {}
    if token:
        headers["X-Vault-Token"] = token
    try:
        response = requests.request(
            method,
            f"{ADDRESS}/v1/{path}",
            headers=headers,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as error:
        raise RuntimeError(f"OpenBao request failed for {path}") from error
    if not response.ok:
        raise RuntimeError(f"OpenBao request failed for {path}: HTTP {response.status_code}")
    if response.status_code == 204:
        return {}
    return response.json()


def configure_secrets_engine(bootstrap_token: str):
    mount_response = api("GET", "sys/mounts", token=bootstrap_token)
    if not isinstance(mount_response, dict):
        raise RuntimeError("OpenBao returned an invalid secrets mount list")
    mounts = mount_response.get("data")
    if not isinstance(mounts, dict):
        raise RuntimeError("OpenBao returned an invalid secrets mount list")

    autopcr_mount = mounts.get("autopcr/")
    if autopcr_mount is None:
        api(
            "POST",
            "sys/mounts/autopcr",
            token=bootstrap_token,
            payload={"type": "kv", "options": {"version": "2"}},
        )
    else:
        mount_options = (
            autopcr_mount.get("options")
            if isinstance(autopcr_mount, dict)
            else None
        )
        if (
            not isinstance(autopcr_mount, dict)
            or autopcr_mount.get("type") != "kv"
            or not isinstance(mount_options, dict)
            or mount_options.get("version") != "2"
        ):
            raise RuntimeError(
                "OpenBao mount 'autopcr/' exists but is not configured as KV v2"
            )

    policy = """
path "autopcr/data/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "autopcr/metadata/*" {
  capabilities = ["read", "delete"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
"""
    api(
        "PUT",
        "sys/policies/acl/autopcr",
        token=bootstrap_token,
        payload={"policy": policy},
    )

    auth_response = api("GET", "sys/auth", token=bootstrap_token)
    if not isinstance(auth_response, dict):
        raise RuntimeError("OpenBao returned an invalid auth method list")
    auth_methods = auth_response.get("data")
    if not isinstance(auth_methods, dict):
        raise RuntimeError("OpenBao returned an invalid auth method list")
    approle_mount = auth_methods.get(f"{APPROLE_MOUNT}/")
    if approle_mount is None:
        api(
            "POST",
            f"sys/auth/{APPROLE_MOUNT}",
            token=bootstrap_token,
            payload={"type": "approle"},
        )
    elif not isinstance(approle_mount, dict) or approle_mount.get("type") != "approle":
        raise RuntimeError(
            f"OpenBao auth mount '{APPROLE_MOUNT}/' is not configured as AppRole"
        )

    api(
        "POST",
        f"auth/{APPROLE_MOUNT}/role/{APPROLE_NAME}",
        token=bootstrap_token,
        payload={
            "token_policies": ["autopcr"],
            "token_no_default_policy": True,
            "token_period": APPROLE_TOKEN_PERIOD,
            "secret_id_ttl": "0",
            "secret_id_num_uses": 0,
        },
    )


def ensure_approle_credentials(bootstrap_token: str):
    role_response = api(
        "GET",
        f"auth/{APPROLE_MOUNT}/role/{APPROLE_NAME}/role-id",
        token=bootstrap_token,
    )
    role_id = role_response.get("data", {}).get("role_id")
    if not isinstance(role_id, str) or not role_id:
        raise RuntimeError("OpenBao did not return an AppRole role ID")
    atomic_write(APPROLE_ROLE_ID_FILE, role_id)

    if APPROLE_SECRET_ID_FILE.is_file() and APPROLE_SECRET_ID_FILE.read_text(
        encoding="utf-8"
    ).strip():
        secret_id = APPROLE_SECRET_ID_FILE.read_text(encoding="utf-8").strip()
        try:
            login = api(
                "POST",
                f"auth/{APPROLE_MOUNT}/login",
                payload={"role_id": role_id, "secret_id": secret_id},
            )
        except RuntimeError:
            logger.info("Stored AppRole Secret ID is invalid; rotating it")
        else:
            auth = login.get("auth", {})
            client_token = auth.get("client_token")
            if isinstance(client_token, str) and client_token:
                token_lookup = api(
                    "POST",
                    "auth/token/lookup",
                    token=bootstrap_token,
                    payload={"token": client_token},
                )
                token_data = token_lookup.get("data", {})
            else:
                token_data = {}
            period = token_data.get("period", 0)
            policies = token_data.get("policies")
            if (
                token_data.get("renewable") is True
                and isinstance(period, (int, float))
                and not isinstance(period, bool)
                and period > 0
                and policies == ["autopcr"]
            ):
                api(
                    "POST",
                    "auth/token/revoke",
                    token=bootstrap_token,
                    payload={"token": client_token},
                )
                return
            logger.info("Stored AppRole Secret ID has an invalid token policy; rotating it")

    response = api(
        "POST",
        f"auth/{APPROLE_MOUNT}/role/{APPROLE_NAME}/secret-id",
        token=bootstrap_token,
        payload={},
    )
    secret_id = response.get("data", {}).get("secret_id")
    if not isinstance(secret_id, str) or not secret_id:
        raise RuntimeError("OpenBao did not return an AppRole secret ID")
    atomic_write(APPROLE_SECRET_ID_FILE, secret_id)


def bootstrap():
    if not INIT_READY_FILE.is_file():
        raise RuntimeError("OpenBao init/unseal service is not ready")
    bootstrap_token = BOOTSTRAP_TOKEN_FILE.read_text(encoding="utf-8").strip()
    if not bootstrap_token:
        raise RuntimeError("OpenBao bootstrap token file is empty")
    configure_secrets_engine(bootstrap_token)
    ensure_approle_credentials(bootstrap_token)
    logger.info("OpenBao configuration reconciled")
    atomic_write(READY_FILE, "ready")


def main():
    READY_FILE.unlink(missing_ok=True)
    try:
        bootstrap()
    except Exception:
        READY_FILE.unlink(missing_ok=True)
        logger.exception("OpenBao one-time bootstrap failed")
        raise
    logger.info("OpenBao one-time bootstrap completed")


if __name__ == "__main__":
    main()
