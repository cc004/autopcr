from json import loads
import asyncio, time
from ..util import aiorequests

async def localValidator(_):
    print('use local validator')

    from .bsgamesdk import captch
    cap = await captch()
    challenge = cap['challenge']
    gt = cap['gt']
    userid = cap['gt_user_id']

    import bili_ticket_gt_python
    gt_obj = bili_ticket_gt_python.ClickPy()
    _type = None
    info = None

    n = 3
    for _ in range(n):
        try:
            _type = gt_obj.get_type(gt, challenge)
            break
        except Exception as e:
            pass

    if _type == 'click':
        (c, s, args) = gt_obj.get_new_c_s_args(gt, challenge)
        st = time.time()
        w = gt_obj.generate_w(gt_obj.calculate_key(args), gt, challenge, str(c), s, "abcdefghijklmnop")
        ed = time.time()
        await asyncio.sleep(max(0, 2 - (ed - st)))
        (msg, validate) = gt_obj.verify(gt, challenge, w)
        info = {
            "challenge": challenge,
            "gt_user_id": userid,
            "validate": validate
        }
    return info

async def remoteValidator(_):
    print('use remote validator')

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
            print(res)
            if "queue_num" in res:
                nu = res["queue_num"]
                if nu >= 35: raise Exception("Captcha failed")

                msg.append(f"queue_num={nu}")
                tim = min(int(nu), 3) * 10
                msg.append(f"sleep={tim}")
                print(f"farm:\n" + "\n".join(msg))
                msg = []
                print(f'farm: {uuid} in queue, sleep {tim} seconds')
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
