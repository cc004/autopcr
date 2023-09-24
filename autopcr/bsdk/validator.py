from ..util import aiorequests, questutils
from json import dumps, loads
import asyncio

validate_dict = {}
validate_ok_dict = {}


async def manualValidator(account, gt, challenge, userid):
    id = questutils.create_quest_token()
    url = f"/daily/geetest.html?id={id}&captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    validate_dict[account] = url
    for _ in range(120):
        if id not in validate_ok_dict:
            await asyncio.sleep(1)
        else:
            info = {
                "challenge": validate_ok_dict[id]['challenge'],
                "gt_user_id": validate_ok_dict[id]['userid'],
                "validate": validate_ok_dict[id]['validate'],
            }
            del validate_ok_dict[id]
            break
    else:
        raise ValueError("验证码验证超时")

    return info


async def autoValidator(account, gt, challenge, userid):
    url = f"https://pcrd.tencentbot.top/geetest_renew?captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    # url = f"http://help.tencentbot.top/geetest?captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    validate = ""
    '''
    url = f"https://help.tencentbot.top/geetest/?captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    print(url)
    validate = input()
    return validate
    '''
    header = {"Content-Type": "application/json", "User-Agent": "autopcr/1.0.0"}
    succ = 0
    info = ""
    ret = None
    print(url)
    # await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: Auto verifying\n欲手动过码，请发送 validate{ordd} manual")
    print(f"farm: Auto verifying")
    try:
        # res = await (await aiorequests.post(url="http://pcrd.tencentbot.top/validate", data=dumps({"url": url}), headers=header)).content
        res = await (await aiorequests.get(url=url, headers=header)).content
        print(res)
        # if str(res.status_code) != "200":
        #    continue
        res = loads(res)
        uuid = res["uuid"]
        msg = [f"uuid={uuid}"]
        ccnt = 0
        ret = None
        while ccnt < 10:
            ccnt += 1
            res = await (await aiorequests.get(url=f"https://pcrd.tencentbot.top/check/{uuid}", headers=header)).content
            # if str(res.status_code) != "200":
            #    continue
            print(res)
            res = loads(res)
            if "queue_num" in res:
                nu = res["queue_num"]
                msg.append(f"queue_num={nu}")
                tim = min(int(nu), 3) * 10
                msg.append(f"sleep={tim}")
                # await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: \n" + "\n".join(msg))
                print(f"farm:\n" + "\n".join(msg))
                msg = []
                print(f'farm: {uuid} in queue, sleep {tim} seconds')
                await asyncio.sleep(tim)
            else:
                info = res["info"]
                if info in ["fail", "url invalid"]:
                    break
                elif info == "in running":
                    await asyncio.sleep(8)
                elif 'validate' in info:
                    ret = info
            if ccnt >= 10:
                break
                raise Exception("Captcha failed")
    except:
        if not ret:
            ret = await manualValidator(account, gt, challenge, userid)
    # await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: succ={succ} validate={validate}")


    # captcha_lck.release()
    # await captcha_lck.acquire()
    return ret
