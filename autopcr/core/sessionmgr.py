from .base import Component, RequestHandler
from .apiclient import apiclient, ApiException
from .sdkclient import sdkclient
import json, os, random
from ..model.models import *
from ..constants import CACHE_DIR
from ..util.logger import instance as logger

class sessionmgr(Component[apiclient]):
    def __init__(self, sdk: sdkclient):
        super().__init__()
        self.cacheDir = os.path.join(CACHE_DIR, 'token')
        self.sdk = sdk
        self._logged = False
        self.auto_relogin = True
        self._sdkaccount = None
        self.session_expire_time = 0
        self.id = self.sdk.session_id
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)

    @property
    def cacheFile(self):
        return os.path.join(self.cacheDir, self.sdk.id)

    async def _bililogin(self):
        uid, access_key = await self.sdk.login()
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
                            platform=str(self.sdk.platform_id),
                            channel_id=str(self.sdk.channel)
                        )
                        if not (await next.request(req)).is_risk:
                            break
                        else:
                            for _ in range(5):
                                captch_done = await self.sdk.do_captcha()
                                req = ToolSdkLoginRequest(
                                    uid=self._sdkaccount['uid'],
                                    access_key=self._sdkaccount['access_key'],
                                    platform=str(self.sdk.platform_id),
                                    channel_id=str(self.sdk.channel),
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
        except Exception as e:
            logger.exception(e)
            raise PanicError(f"登录出错: {e}")
        finally:
            await self.sdk.invoke_post_login()

    async def _login(self, next: RequestHandler):
        if self.sdk.is_tw:
            await self._login_tw(next)
            return

        if os.path.exists(self.cacheFile):
            with open(self.cacheFile, 'r') as fp:
                self._sdkaccount = json.load(fp)
        for _ in range(5):
            try:
                current = self._container.servers[self._container.active_server]
                self._container.servers = [
                    (server if server.startswith(('http://', 'https://')) else f'https://{server}')
                    .replace('\t', '').rstrip('/') + '/'
                    for server in (await next.request(SourceIniIndexRequest())).server
                ]
                try:
                    self._container.active_server = self._container.servers.index(current)
                except ValueError:
                    self._container.active_server = 0
                manifest = await next.request(SourceIniGetMaintenanceStatusRequest())
                self._container._headers['MANIFEST-VER'] = manifest.required_manifest_ver
                
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
                self.session_expire_time = (await next.request(req)).daily_reset_time

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

                req = UnitRoleGachaIndexRequest()
                resp = await next.request(req)

                self._logged = True
                break
            except ApiException as e:
                if any(word in str(e) for word in ("维护", "維護")):
                    raise PanicError(str(e))
                pass
        else:
            raise PanicError("登录失败")

    async def _login_tw(self, next: RequestHandler):
        """Login flow used by So-net Taiwan accounts.

        TW has no source_ini or tool/sdk_login handshake.  The credentials in
        PlayerPrefs are sent directly through the normal encrypted API.
        """
        from ..db.dbstart import ensure_database

        try:
            await next.request(CheckAgreementRequest())

            # Current TW clients send no CN campaign fields here.
            game_start = await next.request(TwCheckGameStartRequest())
            if getattr(game_start, 'bundle_ver', None):
                self._container._headers['BUNDLE-VER'] = str(
                    game_start.bundle_ver
                )
            if not game_start.now_tutorial:
                raise PanicError("账号未完成教程")
            # API responses carry the authoritative resource revision.  Use it
            # for the official manifest/master bundle before response handlers
            # begin consulting regional master data.  The database revision is
            # never copied back into the transport's RES-VER header.
            await ensure_database(
                self.sdk.region,
                self._container._headers.get('RES-VER'),
            )
            req = LoadIndexRequest()
            req.carrier = 'Android'
            load_index = await next.request(req)
            self.session_expire_time = (
                load_index.daily_reset_time
                or self._container.time + 24 * 60 * 60
            )

            req = HomeIndexRequest()
            req.message_id = 1
            req.gold_history = 0
            req.is_first = 1
            req.tips_id_list = []
            resp = await next.request(req)

            if (resp.quest_list and any(
                quest.quest_id == 11008001
                and quest.result_type == eMissionStatusType.AlreadyReceive
                for quest in resp.quest_list
            )):
                req = DailyTaskTopRequest()
                req.setting_alchemy_count = 1
                req.is_check_by_term_normal_gacha = 0
                await next.request(req)

            self._logged = True
        except ApiException as ex:
            if any(word in str(ex) for word in ("维护", "維護")):
                raise PanicError(str(ex)) from ex
            raise PanicError(
                f"台服登录失败，请检查凭证、区服和 APP 版本：{ex}"
            ) from ex
        finally:
            await self.sdk.invoke_post_login()

    @property
    def is_session_expired(self):
        return self._logged and self._container.time >= self.session_expire_time

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
