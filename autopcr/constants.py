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
TWSDK = '台服'

CHANNEL_OPTION = [BSDK, QSDK, BSDKNOLOGIN, TWSDK]

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

# Headers
DEFAULT_HEADERS = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux, U, Android 5.1.1, PCRT00 Build/LMY48Z)',
    'X-Unity-Version': '2021.3.20f1c1',
    'APP-VER': "11.7.1",
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
    'APP-VER': "11.7.1",
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

# Taiwan uses a different transport profile.  APP-VER is intentionally kept
# separate from the CN version cache; it can be updated without affecting CN
# accounts.  RES-VER is refreshed from data_headers.required_res_ver after the
# first successful TW request.
TW_UNITY_VERSION = os.getenv('AUTOPCR_TW_UNITY_VERSION', '6000.0.58f2')
TW_CURL_VERSION = os.getenv('AUTOPCR_TW_CURL_VERSION', '8.10.1-DEV')
TW_USE_SYSTEM_PROXY = os.getenv(
    'AUTOPCR_TW_USE_SYSTEM_PROXY', 'false'
).strip().lower() in {'1', 'true', 'yes', 'on'}
TW_HEADERS = {
    'Accept-Encoding': 'deflate, gzip',
    'User-Agent': f'UnityPlayer/{TW_UNITY_VERSION} (UnityWebRequest/1.0, libcurl/{TW_CURL_VERSION})',
    'Content-Type': 'application/octet-stream',
    'Expect': '100-continue',
    'X-Unity-Version': TW_UNITY_VERSION,
    'APP-VER': os.getenv('AUTOPCR_TW_APP_VERSION', '5.7.0'),
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '2',
    # Empty means derive a stable per-account value from the TW UDID.  An
    # explicit override remains available for migrated installations.
    'DEVICE-ID': os.getenv('AUTOPCR_TW_DEVICE_ID', '').strip(),
    'DEVICE-NAME': 'OPPO PCRM00',
    'GRAPHICS-DEVICE-NAME': 'Adreno (TM) 640',
    'IP-ADDRESS': '10.0.2.15',
    'KEYCHAIN': '',
    'LOCALE': 'Jpn',
    'PLATFORM-OS-VERSION': 'Android OS 5.1.1 / API-22 (LMY48Z/rel.se.infra.20200612.100533)',
    'REGION-CODE': '',
    # RES-VER is the asset/resource revision used by the HTTP protocol.  It is
    # independent from the master_tw.db revision published by database mirrors.
    'RES-VER': os.getenv('AUTOPCR_TW_RES_VERSION', '00500030'),
    'platform': '2',
}


def refresh_headers(version: str = None):
    default_ver = '11.4.0'
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
