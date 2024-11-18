from typing import Dict, List
from ..util import aiorequests, questutils
from ..model.error import PanicError
from json import loads
import asyncio, time
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import defaultdict

@dataclass_json
@dataclass
class ValidateInfo:
    id: str = ""
    challenge: str = ""
    gt: str = ""
    userid: str = ""
    url: str = ""
    status: str = ""
    validate: str = ""

validate_dict: Dict[str, List[ValidateInfo]] = defaultdict(list)
validate_ok_dict: Dict[str, ValidateInfo] = {}

async def Validator(qq):
    info = None
    for validator in [remoteValidator, localValidator, manualValidator]:
        try:
            info = await validator(qq)
            if info:
                break
        except Exception as e:
            import traceback
            traceback.print_exc()
            pass
    if not info:
        raise PanicError("验证码验证超时")
    return info

async def manualValidator(qq):
    print('use manual validator')

    from .bsgamesdk import captch
    cap = await captch()
    challenge = cap['challenge']
    gt = cap['gt']
    userid = cap['gt_user_id']

    id = questutils.create_quest_token()
    url = f"/daily/validate?id={id}&captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    validate_dict[qq].append(ValidateInfo(
            id=id,
            challenge=challenge,
            gt=gt,
            userid=userid,
            url=url,
            status="need validate"
    ))
    info = None
    for _ in range(120):
        if id not in validate_ok_dict:
            await asyncio.sleep(1)
        else:
            info = {
                "challenge": validate_ok_dict[id].challenge,
                "gt_user_id": validate_ok_dict[id].userid,
                "validate" : validate_ok_dict[id].validate
            }
            del validate_ok_dict[id]
            break
    return info


async def localValidator(qq):
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
        cor = asyncio.sleep(2)
        w = gt_obj.generate_w(gt_obj.calculate_key(args), gt, challenge, str(c), s, "abcdefghijklmnop")
        await cor
        (msg, validate) = gt_obj.verify(gt, challenge, w)
        info = {
            "challenge": challenge,
            "gt_user_id": userid,
            "validate": validate
        }
    return info

async def remoteValidator(qq):
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
