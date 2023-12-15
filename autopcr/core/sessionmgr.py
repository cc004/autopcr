from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException
from ..bsdk.bsdkclient import bsdkclient
import json, os, random
from ..model.models import *
from ..constants import CACHE_DIR
import hashlib

class sessionmgr(Component[apiclient]):
    def __init__(self, account, *arg, **kwargs):
        super().__init__()
        self.cacheDir = os.path.join(CACHE_DIR, 'token')
        self.bsdk = bsdkclient(account, *arg, **kwargs)
        self._platform = self.bsdk.platform
        self._channel = self.bsdk.channel
        self._account = account
        self._logged = False
        self.auto_relogin = True
        self._sdkaccount = None
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)
        self.cacheFile = os.path.join(self.cacheDir, hashlib.md5(account['account'].encode('utf-8')).hexdigest())

    def register_to(self, container: apiclient):
        container._headers['PLATFORM'] = str(self._account['platform'])
        container._headers['PLATFORM-ID'] = str(self._account['platform'])
        container._headers['CHANNEL-ID'] = str(self._account['channel'])
        return super().register_to(container)

    async def _bililogin(self):
        uid, access_key = await self.bsdk.login()
        self._sdkaccount = {
                'uid': uid,
                'access_key': access_key
        }
        with open(self.cacheFile, 'w') as fp:
            json.dump(self._sdkaccount, fp)
    
    async def _ensure_token(self, next: RequestHandler):
        while True:
            if self._sdkaccount and self._sdkaccount['access_key']:
                try:
                    req = ToolSdkLoginRequest(
                        uid=self._sdkaccount['uid'],
                        access_key=self._sdkaccount['access_key'],
                        platform=str(self._platform),
                        channel_id=str(self._channel)
                    )
                    if not (await next.request(req)).is_risk:
                        break
                    else:
                        for _ in range(5):
                            from ..bsdk.bsgamesdk import captch
                            cap=await captch()
                            captch_done=await self.bsdk.captchaVerifier(self.bsdk.account, cap['gt'], cap['challenge'], cap['gt_user_id'])
                            req = ToolSdkLoginRequest(
                                uid=self._sdkaccount['uid'],
                                access_key=self._sdkaccount['access_key'],
                                platform=str(self._platform),
                                channel_id=str(self._channel),
                                challenge=captch_done['challenge'],
                                validate_=captch_done['validate'],
                                seccode=captch_done['validate']+"|jordan",
                                captcha_type='1',
                                image_token='',
                                captcha_code='',
                            )
                            if not (await next.request(req)).is_risk:
                                break
                        else:
                            raise ValueError("登录失败，帐号存在风险")
                except ApiException:
                    pass
            
            self._sdkaccount = None
            await self._bililogin()

        from ..bsdk.validator import validate_dict
        validate_dict[self._account['account']] = "ok"

    async def _login(self, next: RequestHandler):
        if os.path.exists(self.cacheFile):
            with open(self.cacheFile, 'r') as fp:
                self._sdkaccount = json.load(fp)
        while True:
            try:
                self._container.servers = [f'http://{server}'.replace('\t', '') for server in (await next.request(SourceIniIndexRequest())).server]
                self._container.active_server = 0
                manifest = await next.request(SourceIniGetMaintenanceStatusRequest())
                self._container._headers['MANIFEST-VER'] = manifest.required_manifest_ver
                if manifest.maintenance_message:
                    raise ValueError(manifest.maintenance_message)
                
                await self._ensure_token(next)
                
                req = CheckGameStartRequest()
                req.apptype = 0
                req.campaign_data = ''
                req.campaign_user = random.randint(0, 100000) & ~1
                
                if not (await next.request(req)).now_tutorial:
                    raise ValueError("账号未过完教程")
                
                # await next.request(CheckAgreementRequest())

                req = LoadIndexRequest()
                req.carrier = "OPPO"
                await next.request(req)

                req = HomeIndexRequest()
                req.message_id = 1
                req.gold_history = 0
                req.is_first = 1
                req.tips_id_list = []
                await next.request(req)

                self._logged = True
                break
            except ApiException:
                pass

    async def request(self, request: Request[TResponse], next: RequestHandler) -> TResponse:
        if not self._logged:
            await self._login(next)
        try:
            return await next.request(request)
        except ApiException as ex:
            if ex.status == 3 and self.auto_relogin:
                self._logged = False
            raise

    async def clear_session(self):
        self._logged = False
