from ..util import aiorequests, freqlimiter
from json import loads
import asyncio
from ..util import aiorequests
from ..util.logger import instance as logger

_gtlv_client = None
_gtlv_client_lock = asyncio.Lock()

async def _get_gtlv_client():
    # 复用同一个 Client：它在首次遇到点选验证码时加载识别模型，这项开销只应付出一次。
    global _gtlv_client
    if _gtlv_client is None:
        async with _gtlv_client_lock:
            if _gtlv_client is None:
                from gtlv import Client
                _gtlv_client = Client(max_attempts=3)
    return _gtlv_client

async def localValidator():
    logger.info('use local validator')

    from .bsgamesdk import captch
    cap = await captch()

    info = None
    try:
        client = await _get_gtlv_client()
        # 必须沿用 start_captcha 下发的这一组 gt/challenge：登录接口不提交 gt，
        # 服务端按自己的 gt 校验 (challenge, validate)，另行登记得到的 validate 不被接受。
        result = await client.solve(cap['gt'], cap['challenge'])
        info = {
            # 滑动流程会换用新的 challenge，须提交 result.challenge 而非传入的那个。
            "challenge": result.challenge,
            "gt_user_id": cap['gt_user_id'],
            "validate": result.validate
        }
        logger.info(f'local validator solved a {result.captcha_type} captcha')
    except Exception as e:
        logger.error(f'local validator error: {e}')

    return info

@freqlimiter.FreqLimiter(5,30)
async def remoteValidator():
    logger.info('use remote validator')

    url = f"https://pcrd.tencentbot.top/geetest_renew"
    header = {"Content-Type": "application/json", "User-Agent": "autopcr/1.0.0"}
    info = ""
    ret = None
    try:
        res = await aiorequests.get(url=url, headers=header)
        res.raise_for_status()
        res = await res.content
        res = loads(res)
        uuid = res["uuid"]
        msg = [f"uuid={uuid}"]
        ccnt = 0
        up = 5
        while ccnt <= up:
            ccnt += 1
            res = await aiorequests.get(url=f"https://pcrd.tencentbot.top/check/{uuid}", headers=header)
            res.raise_for_status()
            res = await res.content
            res = loads(res)
            logger.info(res)
            if "queue_num" in res:
                nu = res["queue_num"]
                if nu >= 35: raise Exception("Captcha failed")

                msg.append(f"queue_num={nu}")
                tim = min(int(nu), 3) * 10
                msg.append(f"sleep={tim}")
                msg = []
                logger.info(f'farm: {uuid} in queue, sleep {tim} seconds')
                await asyncio.sleep(tim)
                if tim >= 40: ccnt += 2
            else:
                info = res["info"]
                if info in ["fail", "url invalid"]:
                    raise Exception("Captcha failed")
                elif info == "in running":
                    await asyncio.sleep(8)
                elif 'validate' in info:
                    ret = info
                    break
        else:
            raise Exception("Captcha failed")
    except:
        pass

    return ret
