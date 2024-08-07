from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException
from .sdkclient import sdkclient
import json, os, random
from ..model.models import *
from ..constants import CACHE_DIR
import hashlib

class sessionmgr(Component[apiclient]):
    def __init__(self, sdk: sdkclient, *arg, **kwargs):
        super().__init__()
        self.cacheDir = os.path.join(CACHE_DIR, 'token')
        self.bsdk = sdk
        self._platform = self.bsdk.platform_id
        self._channel = self.bsdk.channel
        self._account: str = sdk.account
        self._logged = False
        self.auto_relogin = True
        self._sdkaccount = None
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)
        self.cacheFile = os.path.join(self.cacheDir, hashlib.md5(self._account.encode('utf-8')).hexdigest())

    async def _bililogin(self):
        uid, access_key = await self.bsdk.login()
        self._sdkaccount = {
                'uid': uid,
                'access_key': access_key
        }
        with open(self.cacheFile, 'w') as fp:
            json.dump(self._sdkaccount, fp)
    
    async def _ensure_token(self, next: RequestHandler):
        try:
            for _ in range(5):
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
                                captch_done = await self.bsdk.do_captcha()
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
                                raise PanicError("登录失败，帐号存在风险")
                    except ApiException:
                        pass
                
                self._sdkaccount = None
                await self._bililogin()
            else:
                raise PanicError("登录失败")
        except Exception:
            raise
        finally:
            from ..bsdk.validator import validate_dict, ValidateInfo
            validate_dict[self._account] = ValidateInfo(status="ok")

    async def _login(self, next: RequestHandler):
        if os.path.exists(self.cacheFile):
            with open(self.cacheFile, 'r') as fp:
                self._sdkaccount = json.load(fp)
        while True:
            try:
                current = self._container.servers[self._container.active_server]
                self._container.servers = [f'https://{server}'.replace('\t', '') for server in (await next.request(SourceIniIndexRequest())).server]
                try:
                    self._container.active_server = self._container.servers.index(current)
                except ValueError:
                    self._container.active_server = 0
                manifest = await next.request(SourceIniGetMaintenanceStatusRequest())
                self._container._headers['MANIFEST-VER'] = manifest.required_manifest_ver
                if manifest.maintenance_message:
                    raise PanicError(manifest.maintenance_message)
                
                await self._ensure_token(next)
                
                req = CheckGameStartRequest()
                req.apptype = 0
                req.campaign_data = ''
                req.campaign_user = random.randint(0, 100000) & ~1
                
                if not (await next.request(req)).now_tutorial:
                    raise PanicError("账号未过完教程")
                
                # await next.request(CheckAgreementRequest())

                req = LoadIndexRequest()
                req.carrier = "OPPO"
                await next.request(req)

                req = HomeIndexRequest()
                req.message_id = 1
                req.gold_history = 0
                req.is_first = 1
                req.tips_id_list = []
                resp = await next.request(req)

                if resp.quest_list and any(1 for quest in resp.quest_list if quest.quest_id == 11008001 and quest.result_type == eMissionStatusType.AlreadyReceive): # clear normal 8-1 and unlock daily task
                    req = DailyTaskTopRequest()
                    req.setting_alchemy_count = 1
                    req.is_check_by_term_normal_gacha = 0
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
