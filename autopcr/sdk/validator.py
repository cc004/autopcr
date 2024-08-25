from typing import Dict
from ..util import aiorequests, questutils
from ..model.error import PanicError
from json import loads
import asyncio, time
from dataclasses import dataclass
from dataclasses_json import dataclass_json

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

validate_dict: Dict[str, ValidateInfo] = {}
validate_ok_dict: Dict[str, ValidateInfo] = {}

async def Validator(account):
    from .bsgamesdk import captch
    print('use local validator')
    cap = await captch()
    info = await localValidator(account, cap['gt'], cap['challenge'], cap['gt_user_id'])
    if not info:
        print('use remote validator')
        info = await remoteValidator()
    if not info:
        print('use manual validator')
        cap = await captch()
        info = await manualValidator(account, cap["gt"], cap["challenge"], cap["gt_user_id"])
    if not info:
        raise PanicError("验证码验证超时")
    return info

async def manualValidator(account, gt, challenge, userid):
    id = questutils.create_quest_token()
    url = f"/daily/validate?id={id}&captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    validate_dict[account] = ValidateInfo(
            id=id,
            challenge=challenge,
            gt=gt,
            userid=userid,
            url=url,
            status="need validate"
    )
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

import bili_ticket_gt_python

async def localValidator(account, gt, challenge, userid):
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

async def remoteValidator():
    url = f"https://pcrd.tencentbot.top/geetest_renew"
    header = {"Content-Type": "application/json", "User-Agent": "autopcr/1.0.0"}
    info = ""
    print(f"farm: Auto verifying")
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
