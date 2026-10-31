import asyncio
import logging
import re
import time
from urllib.parse import quote

import requests

from .constants import (
    OPENBAO_ADDR,
    OPENBAO_APPROLE_MOUNT,
    OPENBAO_AUTH_METHOD,
    OPENBAO_K8S_JWT_FILE,
    OPENBAO_K8S_MOUNT,
    OPENBAO_K8S_ROLE,
    OPENBAO_ROLE_ID,
    OPENBAO_ROLE_ID_FILE,
    OPENBAO_SECRET_ID_FILE,
    OPENBAO_TOKEN_FILE,
)
from .util import aiorequests


logger = logging.getLogger(__name__)


class OpenBaoError(Exception):
    pass


class OpenBaoClient:
    def __init__(self):
        self.address = OPENBAO_ADDR.rstrip("/")
        self.auth_method = OPENBAO_AUTH_METHOD
        self.token_file = OPENBAO_TOKEN_FILE
        self.role_id = OPENBAO_ROLE_ID
        self.role_id_file = OPENBAO_ROLE_ID_FILE
        self.secret_id_file = OPENBAO_SECRET_ID_FILE
        self.approle_mount = OPENBAO_APPROLE_MOUNT
        self.kubernetes_role = OPENBAO_K8S_ROLE
        self.kubernetes_mount = OPENBAO_K8S_MOUNT
        self.kubernetes_jwt_file = OPENBAO_K8S_JWT_FILE
        self._approle_token = None
        self._approle_token_expires_at = 0.0
        self._approle_token_renewable = False
        self._approle_lock = asyncio.Lock()
        self._connected = False
        self._renewal_task = None
        self._last_forbidden_reauth_at = None
        self._last_login_failure_at = None
        self._reauth_cooldown = 5

    def _read_token_file(self) -> str:
        try:
            with open(self.token_file, "r") as token_file:
                token = token_file.read().strip()
        except OSError as error:
            raise OpenBaoError("OpenBao application token is unavailable") from error
        if not token:
            raise OpenBaoError("OpenBao application token is empty")
        return token

    def _read_secret_id(self) -> str:
        try:
            with open(self.secret_id_file, "r") as secret_id_file:
                secret_id = secret_id_file.read().strip()
        except OSError as error:
            raise OpenBaoError("OpenBao AppRole secret ID is unavailable") from error
        if not secret_id:
            raise OpenBaoError("OpenBao AppRole secret ID is empty")
        return secret_id

    def _read_role_id(self) -> str:
        if self.role_id:
            return self.role_id
        try:
            with open(self.role_id_file, "r") as role_id_file:
                role_id = role_id_file.read().strip()
        except OSError as error:
            raise OpenBaoError("OpenBao AppRole role ID is unavailable") from error
        if not role_id:
            raise OpenBaoError("OpenBao AppRole role ID is empty")
        return role_id

    def _read_kubernetes_jwt(self) -> str:
        try:
            with open(self.kubernetes_jwt_file, "r") as jwt_file:
                jwt = jwt_file.read().strip()
        except OSError as error:
            raise OpenBaoError("Kubernetes ServiceAccount JWT is unavailable") from error
        if not jwt:
            raise OpenBaoError("Kubernetes ServiceAccount JWT is empty")
        return jwt

    async def _send(self, method: str, path: str, payload=None, token=None):
        headers = {"X-Vault-Token": token} if token else {}
        try:
            return await aiorequests.request(
                method,
                f"{self.address}/v1/{path}",
                json=payload,
                headers=headers,
                timeout=15,
            )
        except requests.RequestException as error:
            raise OpenBaoError(f"OpenBao request failed for {path}") from error

    async def _response_json(self, response, path):
        if not response.ok:
            raise OpenBaoError(
                f"OpenBao request failed for {path}: HTTP {response.status_code}"
            )
        if response.status_code == 204:
            return {}
        try:
            return await response.json()
        except (ValueError, requests.RequestException) as error:
            raise OpenBaoError(f"OpenBao returned invalid JSON for {path}") from error

    async def _auth_login(self):
        if self.auth_method == "approle":
            path = f"auth/{self.approle_mount}/login"
            payload = {
                "role_id": self._read_role_id(),
                "secret_id": self._read_secret_id(),
            }
        elif self.auth_method == "kubernetes":
            path = f"auth/{self.kubernetes_mount}/login"
            payload = {
                "role": self.kubernetes_role,
                "jwt": self._read_kubernetes_jwt(),
            }
        else:
            raise OpenBaoError(f"Unsupported OpenBao authentication method: {self.auth_method}")
        result = await self._send("POST", path, payload)
        try:
            auth = (await self._response_json(result, path))["auth"]
            token = auth["client_token"]
            lease_duration = auth["lease_duration"]
            renewable = auth["renewable"]
        except (KeyError, TypeError) as error:
            raise OpenBaoError("OpenBao returned an invalid authentication login response") from error
        if (
            not isinstance(token, str)
            or not token
            or not isinstance(lease_duration, (int, float))
            or lease_duration <= 0
            or not isinstance(renewable, bool)
        ):
            raise OpenBaoError("OpenBao returned an invalid authentication token lease")
        self._approle_token = token
        self._approle_token_expires_at = time.monotonic() + lease_duration
        self._approle_token_renewable = bool(renewable)
        return token

    async def _renew_auth_token(self):
        result = await self._send(
            "POST",
            "auth/token/renew-self",
            token=self._approle_token,
        )
        try:
            auth = (await self._response_json(result, "auth/token/renew-self"))["auth"]
            token = auth["client_token"]
            lease_duration = auth["lease_duration"]
            renewable = auth["renewable"]
        except (KeyError, TypeError) as error:
            raise OpenBaoError("OpenBao returned an invalid authentication renewal response") from error
        if (
            not isinstance(token, str)
            or not token
            or not isinstance(lease_duration, (int, float))
            or lease_duration <= 0
            or not isinstance(renewable, bool)
        ):
            raise OpenBaoError("OpenBao returned an invalid renewed token lease")
        self._approle_token = token
        self._approle_token_expires_at = time.monotonic() + lease_duration
        self._approle_token_renewable = bool(renewable)
        return token

    async def connect(self):
        if self._connected:
            return
        if self.auth_method == "token":
            token = self._read_token_file()
            response = await self._send(
                "GET",
                "auth/token/lookup-self",
                token=token,
            )
            await self._response_json(response, "auth/token/lookup-self")
        elif self.auth_method in ("approle", "kubernetes"):
            await self._auth_login()
        else:
            raise OpenBaoError(
                f"Unsupported OpenBao authentication method: {self.auth_method}"
            )
        self._connected = True
        logger.info("Connected to OpenBao using %s authentication", self.auth_method)

    def start_background_tasks(self):
        if (
            self.auth_method in ("approle", "kubernetes")
            and self._renewal_task is None
        ):
            self._renewal_task = asyncio.create_task(self._token_renewal_loop())

    async def _login_with_cooldown(self):
        now = time.monotonic()
        if (
            self._last_login_failure_at is not None
            and now - self._last_login_failure_at < self._reauth_cooldown
        ):
            raise OpenBaoError("OpenBao login retry is temporarily rate-limited")
        try:
            token = await self._auth_login()
        except OpenBaoError:
            self._last_login_failure_at = now
            raise
        self._last_login_failure_at = None
        return token

    async def _token_renewal_loop(self):
        while True:
            await asyncio.sleep(60)
            if not self._approle_token:
                try:
                    async with self._approle_lock:
                        await self._login_with_cooldown()
                except OpenBaoError:
                    logger.exception("Failed to log in to OpenBao during token maintenance")
                continue

            async with self._approle_lock:
                remaining = self._approle_token_expires_at - time.monotonic()
                if remaining > 60:
                    continue
                if self._approle_token_renewable and remaining > 0:
                    try:
                        await self._renew_auth_token()
                    except OpenBaoError:
                        logger.exception("Failed to renew OpenBao authentication token")
                        try:
                            await self._login_with_cooldown()
                        except OpenBaoError:
                            logger.exception("Failed to reauthenticate to OpenBao")
                else:
                    try:
                        await self._login_with_cooldown()
                    except OpenBaoError:
                        logger.exception("Failed to log in to OpenBao during token maintenance")

    async def _token(self) -> str:
        if self.auth_method == "token":
            return self._read_token_file()
        if self.auth_method not in ("approle", "kubernetes"):
            raise OpenBaoError(f"Unsupported OpenBao authentication method: {self.auth_method}")

        async with self._approle_lock:
            remaining = self._approle_token_expires_at - time.monotonic()
            if self._approle_token and remaining > 60:
                return self._approle_token
            if self._approle_token and remaining > 0:
                if self._approle_token_renewable:
                    try:
                        return await self._renew_auth_token()
                    except OpenBaoError:
                        logger.exception(
                            "Failed to renew OpenBao token before a request; "
                            "attempting to reauthenticate"
                        )
                        self._approle_token = None
                        return await self._login_with_cooldown()
                else:
                    return self._approle_token
            self._approle_token = None
            return await self._login_with_cooldown()

    async def _reauthenticate_after_forbidden(self, rejected_token):
        async with self._approle_lock:
            if self._approle_token and self._approle_token != rejected_token:
                return self._approle_token

            now = time.monotonic()
            if (
                self._last_forbidden_reauth_at is not None
                and now - self._last_forbidden_reauth_at < self._reauth_cooldown
            ):
                return None
            self._last_forbidden_reauth_at = now
            return await self._login_with_cooldown()

    async def _request(self, method: str, path: str, payload=None, allow_missing=False):
        token = await self._token()
        response = await self._send(method, path, payload, token)
        if response.status_code == 403 and self.auth_method in ("approle", "kubernetes"):
            token = await self._reauthenticate_after_forbidden(token)
            if token is not None:
                response = await self._send(method, path, payload, token)
        if allow_missing and response.status_code == 404:
            return None
        return await self._response_json(response, path)

    @staticmethod
    def _secret_path(qid: str, account: str) -> str:
        return f"autopcr/data/{quote(qid, safe='')}/{quote(account, safe='')}"

    @staticmethod
    def _session_path(session_id: str) -> str:
        if not re.fullmatch(r"[a-f0-9]{32}", session_id):
            raise OpenBaoError("Invalid game session identifier")
        return f"autopcr/data/game-sessions/{session_id}"

    async def read_game_session(self, session_id: str):
        result = await self._request(
            "GET",
            self._session_path(session_id),
            allow_missing=True,
        )
        if result is None:
            return None
        try:
            session = result["data"]["data"]
        except (KeyError, TypeError) as error:
            raise OpenBaoError("OpenBao returned an invalid game session record") from error
        if not isinstance(session, dict):
            raise OpenBaoError("OpenBao returned an invalid game session record")
        uid = session.get("uid")
        access_key = session.get("access_key")
        if not isinstance(uid, str) or not isinstance(access_key, str):
            raise OpenBaoError("OpenBao returned invalid game session credentials")
        return {"uid": uid, "access_key": access_key}

    async def write_game_session(self, session_id: str, uid: str, access_key: str):
        if (
            not isinstance(uid, (str, int))
            or isinstance(uid, bool)
            or not isinstance(access_key, str)
        ):
            raise OpenBaoError("Invalid game session credentials")
        await self._request(
            "POST",
            self._session_path(session_id),
            {"data": {"uid": str(uid), "access_key": access_key}},
        )

    async def read_game_credentials(self, qid: str, account: str):
        result = await self._request(
            "GET",
            self._secret_path(qid, account),
            allow_missing=True,
        )
        if result is None:
            return None
        try:
            credentials = result["data"]["data"]
        except (KeyError, TypeError) as error:
            raise OpenBaoError("OpenBao returned an invalid credentials record") from error
        if not isinstance(credentials, dict):
            raise OpenBaoError("OpenBao returned an invalid credentials record")
        username = credentials.get("username", "")
        password = credentials.get("password", "")
        if not isinstance(username, str) or not isinstance(password, str):
            raise OpenBaoError("OpenBao returned invalid game credentials")
        return {"username": username, "password": password}

    async def write_game_credentials(self, qid: str, account: str, username: str, password: str):
        await self._request(
            "POST",
            self._secret_path(qid, account),
            {"data": {"username": username, "password": password}},
        )

    async def delete_game_credentials(self, qid: str, account: str):
        path = self._secret_path(qid, account).replace("/data/", "/metadata/", 1)
        await self._request("DELETE", path, allow_missing=True)


instance = OpenBaoClient()
