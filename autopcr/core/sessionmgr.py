from .base import Component
from .apiclient import apiclient, ApiException
from typing import Callable, Coroutine, Any
from ..bsdk.bsdkclient import bsdkclient
import asyncio, json, re, os, random
import dateutil.parser
from datetime import datetime
from ..model.models import *
from traceback import print_exc

class sessionmgr(Component[apiclient]):
    def __init__(self, account, *arg, **kwargs):
        super().__init__()
        self.cacheDir = os.path.join(os.path.dirname(__file__), 'cache')
        self.bsdk = bsdkclient(account, *arg, **kwargs)
        self._platform = self.bsdk.platform
        self._channel = self.bsdk.channel
        self._account = account
        self._logged = False
        self.auto_relogin = True
        self._sdkaccount = None
        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)
        self.cacheFile = os.path.join(self.cacheDir, account['account'])

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
    
    async def request(self, request: Request[TResponse], next: Callable[[Request[TResponse]], Coroutine[Any, Any, TResponse]]) -> TResponse:
        async def login():
            if os.path.exists(self.cacheFile):
                with open(self.cacheFile, 'r') as fp:
                    self._sdkaccount = json.load(fp)
            while True:
                try:
                    while True:
                        self._container.urlroot = f'http://{(await next(SourceIniIndexRequest())).server[0]}'.replace('\t', '')
                        manifest: SourceIniGetMaintenanceStatusResponse = await next(SourceIniGetMaintenanceStatusRequest())
                        self._container._headers['MANIFEST-VER'] = manifest.required_manifest_ver
                        if not manifest.maintenance_message: break
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', manifest.maintenance_message)
                        if match is not None:
                            end = dateutil.parser.parse(match.group())
                            raise ValueError(f"当前处于维护期间，维护至{end}")
                            while datetime.now() < end:
                                await asyncio.sleep(1)
                        else:
                            await asyncio.sleep(60)

                    while True:
                        if self._sdkaccount and self._sdkaccount['access_key']:
                            req = ToolSdkLoginRequest(
                                uid=self._sdkaccount['uid'],
                                access_key=self._sdkaccount['access_key'],
                                platform=str(self._platform),
                                channel_id=str(self._channel)
                            )
                            if not (await next(req)).is_risk:
                                break
                        
                        self._sdkaccount = None
                        await self._bililogin()

                    req = CheckGameStartRequest()
                    req.apptype = 0
                    req.campaign_data = ''
                    req.campaign_user = random.randint(0, 100000) & ~1
                    if not (await next(req)).now_tutorial:
                        raise Exception("账号未过完教程")
                    
                    await next(CheckAgreementRequest())

                    req = LoadIndexRequest()
                    req.carrier = "OPPO"
                    await next(req)

                    req = HomeIndexRequest()
                    req.message_id = 1
                    req.gold_history = 0
                    req.is_first = 1
                    req.tips_id_list = []
                    await next(req)

                    self._logged = True
                    break
                except ApiException:
                    pass
        if not self._logged:
            await login()
        try:
            return await next(request)
        except ApiException as ex:
            if ex.status == 3 and self.auto_relogin:
                self._logged = False
            raise
