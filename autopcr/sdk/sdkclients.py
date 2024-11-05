from .bsgamesdk import login
from ..model.error import PanicError
from ..core.sdkclient import sdkclient
from ..constants import BSDK, QSDK

class bsdkclient(sdkclient):
    async def login(self):
        while True:
            resp = await login(
                self._account.username,
                self._account.password,
                self.captchaVerifier
            )
            if resp['code'] == 0:
                await self.errlogger("geetest or captcha succeed")
                break
            await self.errlogger(resp['message'])
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
                  
sdkclients = {
    BSDK: bsdkclient,
    QSDK: qsdkclient
}

def create(channel, *args, **kwargs) -> sdkclient:
    if channel not in sdkclients:
        raise ValueError(f"Invalid channel {channel}")
    return sdkclients[channel](*args, **kwargs)
