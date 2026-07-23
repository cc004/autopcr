from .bsgamesdk import login
from ..model.error import PanicError
from ..core.sdkclient import sdkclient
from ..constants import (
    BSDK, BSDKNOLOGIN, QSDK, TWSDK, TW_HEADERS,
    TW_USE_SYSTEM_PROXY,
)
from copy import deepcopy
import hashlib
import os
import re
import uuid

class bsdkclient(sdkclient):
    async def login(self):
        while True:
            resp = await login(
                self._account.username,
                self._account.password,
                self.captchaVerifier
            )
            if resp['code'] == 0:
                self.logger.info("geetest or captcha succeed")
                break
            self.logger.error(resp['message'])
            raise PanicError(resp['message'])

        return resp['uid'], resp['access_key']

    @property
    def apiroot(self):
        return 'https://l3-prod-all-gs-gzlj.bilibiligame.net/'

    @property
    def platform_id(self) -> str:
        return str(self.platform)
    
    @property
    def reskey(self):
        return 'ab00a0a6dd915a052a2ef7fd649083e5'
 
class bsdkclientWithoutLogin(bsdkclient):
    async def login(self):
        return self._account.username, self._account.password
    
class qsdkclient(sdkclient):
    async def login(self):
        return self._account.username, self._account.password

    @property
    def apiroot(self):
        return 'https://l1-prod-uo-gs-gzlj.bilibiligame.net/'

    @property
    def platform_id(self):
        return '4'
    
    @property
    def reskey(self):
        return 'd145b29050641dac2f8b19df0afe0e59'

    async def do_captcha(self):
        raise NotImplementedError


class twsdkclient(sdkclient):
    """Credential/profile holder for the Taiwan game server.

    The web UI only has username/password fields.  For compatibility it may
    store SHORT_UDID as username and ``UDID:VIEWER_ID:SERVER_ID`` as password.
    API users can instead provide viewer_id/server_id as explicit AccountData
    fields and keep password equal to UDID.
    """

    def __init__(self, info, *args, **kwargs):
        super().__init__(info, *args, **kwargs)

        raw_udid = info.password.strip()
        viewer_id = info.viewer_id.strip()
        server_id = info.server_id

        # Parse the composite form even when explicit fields are present.  The
        # explicit values win, which makes account edits/migrations predictable.
        parts = raw_udid.rsplit(':', 2)
        if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            raw_udid, embedded_viewer_id, parsed_server_id = parts
            viewer_id = viewer_id or embedded_viewer_id
            server_id = server_id or int(parsed_server_id)

        if (
            not viewer_id
            or not viewer_id.isdigit()
            or len(viewer_id) > 20
        ):
            raise ValueError(
                '台服需要 VIEWER_ID；请将密码填写为 UDID:VIEWER_ID:TW_SERVER_ID'
            )

        try:
            self.udid = str(uuid.UUID(raw_udid.strip().lower()))
        except (ValueError, AttributeError) as ex:
            raise ValueError('台服 UDID 必须是 32 位或带横线的 36 位 UUID') from ex

        self.short_udid = info.username.strip()
        if not self.short_udid:
            raise ValueError('台服 SHORT_UDID 不能为空')
        if not self.short_udid.isdigit() or len(self.short_udid) > 20:
            raise ValueError('台服 SHORT_UDID 必须是 1 至 20 位数字')

        self.viewer_id = str(viewer_id)
        if not server_id:
            inferred = int(self.viewer_id[0])
            server_id = inferred if inferred in (1, 2, 3, 4) else 0
        if server_id not in (1, 2, 3, 4):
            raise ValueError('台服 TW_SERVER_ID 必须是 1、2、3 或 4')
        self.server_id = int(server_id)
        self.app_version = str(info.app_version or TW_HEADERS['APP-VER'])
        self.use_system_proxy = TW_USE_SYSTEM_PROXY
        if not re.fullmatch(r'\d+\.\d+\.\d+', self.app_version):
            raise ValueError('台服 APP_VERSION 必须为 x.y.z 格式')

        override_root = os.getenv('AUTOPCR_TW_API_ROOT', '').strip()
        primary = (
            'https://api-pc.so-net.tw/'
            if self.server_id == 1
            else 'https://api5-pc.so-net.tw/'
        )
        legacy = (
            'https://api-pc.so-net.tw/'
            if self.server_id == 1
            else f'https://api{self.server_id}-pc.so-net.tw/'
        )
        roots = [override_root, primary, legacy]
        self.apiroots = []
        for root in roots:
            if root:
                root = root.rstrip('/') + '/'
                if root not in self.apiroots:
                    self.apiroots.append(root)

    async def login(self):
        # TW credentials already represent a game session; sessionmgr performs
        # check_agreement -> game_start -> load/index directly.
        return self.viewer_id, ''

    def header(self):
        headers = deepcopy(TW_HEADERS)
        headers['APP-VER'] = self.app_version
        if not headers['DEVICE-ID']:
            headers['DEVICE-ID'] = hashlib.md5(
                self.udid.encode('utf-8')
            ).hexdigest()
        headers['SID'] = hashlib.md5(
            (self.viewer_id + self.udid + 'r!I@nt8e5i=').encode('utf-8')
        ).hexdigest()
        return headers

    @property
    def apiroot(self):
        return self.apiroots[0]

    @property
    def platform_id(self) -> str:
        return '2'

    @property
    def reskey(self):
        return ''

    @property
    def region(self) -> str:
        return 'tw'

    @property
    def is_tw(self) -> bool:
        return True

    @property
    def initial_uid(self):
        return self.viewer_id

    @property
    def account(self):
        # Do not use SHORT_UDID as a public/cache identity.
        return self.viewer_id

    @property
    def session_id(self) -> str:
        return hashlib.md5(
            f'tw:{self.server_id}:{self.viewer_id}'.encode('utf-8')
        ).hexdigest()

    @property
    def id(self):
        return hashlib.md5(
            (
                f'tw:{self.server_id}:{self.viewer_id}:'
                f'{self.short_udid}:{self.udid}'
            ).encode('utf-8')
        ).hexdigest()

    @property
    def pool_key(self):
        return (
            self.id,
            type(self).__name__,
            self.app_version,
            tuple(self.apiroots),
        )
                  
sdkclients = {
    BSDK: bsdkclient,
    QSDK: qsdkclient,
    BSDKNOLOGIN: bsdkclientWithoutLogin,
    TWSDK: twsdkclient,
}

def create(channel, *args, **kwargs) -> sdkclient:
    if channel not in sdkclients:
        raise ValueError(f"Invalid channel {channel}")
    return sdkclients[channel](*args, **kwargs)
