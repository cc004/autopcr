import os
try:
    from distutils.util import strtobool
except ImportError:
    from setuptools._distutils.util import strtobool
import uuid
import logging

SERVER_PORT = int(os.getenv("AUTOPCR_SERVER_PORT", "13200"))
SERVER_HOST = os.getenv("AUTOPCR_SERVER_HOST", "0.0.0.0")

CLIENT_POOL_SIZE_MAX = 100
CLIENT_POOL_MAX_AGE = 3600 * 24
CLIENT_POOL_MAX_CLIENT_ALIVE = 10
CLIENT_POOL_MAX_FARMER_CLIENT_ALIVE = 2
SESSION_ERROR_MAX_RETRY = 2
MAX_API_RUNNING = 8

BSDK = '官服'
QSDK = '渠道服'
BSDKNOLOGIN = '官服免登录'

CHANNEL_OPTION = [BSDK, QSDK, BSDKNOLOGIN]

DEBUG_LOG = strtobool(os.getenv("AUTOPCR_SERVER_DEBUG_LOG", "false"))

ALLOW_REGISTER = strtobool(os.getenv("AUTOPCR_SERVER_ALLOW_REGISTER", 'true'))
SUPERUSER = str(os.getenv("AUTOPCR_SERVER_SUPERUSER", ""))

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
CACHE_DIR = os.path.join(ROOT_DIR, './cache/')
RESULT_DIR = os.path.join(ROOT_DIR, './result/')
DATA_DIR = os.path.join(ROOT_DIR, './data/')
CONFIG_PATH = os.path.join(CACHE_DIR, './http_server/') 
OLD_CONFIG_PATH = os.path.join(ROOT_DIR, 'autopcr/http_server/config')
CLAN_BATTLE_FORBID_PATH = os.path.join(CONFIG_PATH, 'clan_battle_forbidden.txt')

LOG_PATH = os.path.join(ROOT_DIR, 'log/')
LOG_LEVEL = logging.INFO

UUID_NAMESPACE = uuid.UUID("83a3e9e1-2690-4ff2-88bb-075ba6a6743c")

# Public access address for QQ bot messages (e.g., "example.com" or "1.2.3.4:13200")
PUBLIC_ADDRESS = os.getenv("AUTOPCR_PUBLIC_ADDRESS", "")
USE_HTTPS = strtobool(os.getenv("AUTOPCR_USE_HTTPS", "false"))


def _load_hoshino_plugin_config():
    if os.getenv("AUTOPCR_HOSHINO_PLUGIN_MODE") != "true":
        return None

    import hoshino

    return getattr(hoshino.config, "autopcr", None)


_plugin_config = _load_hoshino_plugin_config()


def _openbao_setting(environment_name, config_name, default=""):
    if _plugin_config is not None and hasattr(_plugin_config, config_name):
        return getattr(_plugin_config, config_name)
    return os.getenv(environment_name, default)


OPENBAO_ADDR = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_ADDR",
        "AUTOPCR_OPENBAO_ADDR",
        "http://127.0.0.1:8200",
    )
).strip().rstrip("/")
OPENBAO_TOKEN_FILE = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_TOKEN_FILE",
        "AUTOPCR_OPENBAO_TOKEN_FILE",
        os.path.join(CACHE_DIR, "openbao", "app-token"),
    )
).strip()
OPENBAO_AUTH_METHOD = str(
    _openbao_setting("AUTOPCR_OPENBAO_AUTH_METHOD", "AUTOPCR_OPENBAO_AUTH_METHOD", "token")
).strip().lower()
OPENBAO_ROLE_ID = str(
    _openbao_setting("AUTOPCR_OPENBAO_ROLE_ID", "AUTOPCR_OPENBAO_ROLE_ID", "")
).strip()
OPENBAO_ROLE_ID_FILE = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_ROLE_ID_FILE",
        "AUTOPCR_OPENBAO_ROLE_ID_FILE",
        os.path.join(CACHE_DIR, "openbao", "role-id"),
    )
).strip()
OPENBAO_SECRET_ID_FILE = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_SECRET_ID_FILE",
        "AUTOPCR_OPENBAO_SECRET_ID_FILE",
        os.path.join(CACHE_DIR, "openbao", "secret-id"),
    )
).strip()
OPENBAO_APPROLE_MOUNT = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_APPROLE_MOUNT",
        "AUTOPCR_OPENBAO_APPROLE_MOUNT",
        "approle",
    )
).strip("/")
OPENBAO_K8S_ROLE = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_K8S_ROLE",
        "AUTOPCR_OPENBAO_K8S_ROLE",
        "",
    )
).strip()
OPENBAO_K8S_MOUNT = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_K8S_MOUNT",
        "AUTOPCR_OPENBAO_K8S_MOUNT",
        "kubernetes",
    )
).strip("/")
OPENBAO_K8S_JWT_FILE = str(
    _openbao_setting(
        "AUTOPCR_OPENBAO_K8S_JWT_FILE",
        "AUTOPCR_OPENBAO_K8S_JWT_FILE",
        "/var/run/secrets/kubernetes.io/serviceaccount/token",
    )
).strip()
if OPENBAO_AUTH_METHOD not in ("token", "approle", "kubernetes"):
    raise ValueError(
        "AUTOPCR_OPENBAO_AUTH_METHOD must be 'token', 'approle', or 'kubernetes'"
    )
if OPENBAO_AUTH_METHOD == "token" and not OPENBAO_TOKEN_FILE:
    raise ValueError("Token authentication requires AUTOPCR_OPENBAO_TOKEN_FILE")
if OPENBAO_AUTH_METHOD == "approle" and not (
    (OPENBAO_ROLE_ID or OPENBAO_ROLE_ID_FILE) and OPENBAO_SECRET_ID_FILE
):
    raise ValueError(
        "AppRole authentication requires AUTOPCR_OPENBAO_ROLE_ID or "
        "AUTOPCR_OPENBAO_ROLE_ID_FILE and "
        "AUTOPCR_OPENBAO_SECRET_ID_FILE"
    )
if OPENBAO_AUTH_METHOD == "approle" and not OPENBAO_APPROLE_MOUNT:
    raise ValueError("AppRole authentication requires a non-empty auth mount")
if OPENBAO_AUTH_METHOD == "kubernetes" and not OPENBAO_K8S_ROLE:
    raise ValueError("Kubernetes authentication requires AUTOPCR_OPENBAO_K8S_ROLE")
if OPENBAO_AUTH_METHOD == "kubernetes" and not OPENBAO_K8S_MOUNT:
    raise ValueError("Kubernetes authentication requires a non-empty auth mount")
# Headers
DEFAULT_HEADERS = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux, U, Android 5.1.1, PCRT00 Build/LMY48Z)',
    'X-Unity-Version': '2021.3.20f1c1',
    'APP-VER': "11.7.2",
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '2',
    'DEVICE-NAME': 'OPPO PCRT00',
    'EXCEL-VER': '1.0.0',
    'GRAPHICS-DEVICE-NAME': 'Adreno (TM) 640',
    'IP-ADDRESS': '10.0.2.15',
    'KEYCHAIN': '',
    'LOCALE': 'CN',
    'PLATFORM-OS-VERSION': 'Android OS 5.1.1 / API-22 (LMY48Z/rel.se.infra.20200612.100533)',
    'REGION-CODE': '',
    # 'RES-KEY': 'ab00a0a6dd915a052a2ef7fd649083e5',
    'RES-VER': '10002200',
    'SHORT-UDID': '0'
}

IOS_HEADERS = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'priconne/24 CFNetwork/1492.0.1 Darwin/23.3.0',
    'X-Unity-Version': '2021.3.20f1c1',
    'APP-VER': "11.7.2",
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '1',
    'DEVICE-NAME': 'iPad13,8',
    'EXCEL-VER': '1.0.0',
    'GRAPHICS-DEVICE-NAME': 'Apple M1',
    'IP-ADDRESS': '172.26.62.98',
    'KEYCHAIN': '',
    'LOCALE': 'CN',
    'PLATFORM-OS-VERSION': 'iOS 17.3',
    'REGION-CODE': '',
    # 'RES-KEY': 'ab00a0a6dd915a052a2ef7fd649083e5',
    'RES-VER': '10002200',
    'SHORT-UDID': '0'
}


def refresh_headers(version: str = None):
    default_ver = '11.7.2'
    if version is not None:
        with open(os.path.join(CACHE_DIR, 'version.txt'), 'w', encoding='utf-8') as f:
            f.write(version)
            VERSION = version
    else:
        try:
            with open(os.path.join(CACHE_DIR, 'version.txt'), 'r', encoding='utf-8') as f:
                VERSION = f.read()
        except FileNotFoundError:
            refresh_headers(default_ver)
            return

    DEFAULT_HEADERS['APP-VER'] = VERSION
    IOS_HEADERS['APP-VER'] = VERSION


refresh_headers()
