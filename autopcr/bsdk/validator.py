from ..util import aiorequests
from json import dumps, loads
import asyncio

validate_queue = asyncio.Queue()
validate_ok_queue = asyncio.Queue()

async def manualValidator(gt, challenge, userid):
    await validate_queue.put((challenge, gt, userid))
    validate = await validate_ok_queue.get()
    if validate == "xcwcancle":
        raise ValueError("登录被终止")
    return validate

async def autoValidator(gt, challenge, userid):
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
    print(url)
    #await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: Auto verifying\n欲手动过码，请发送 validate{ordd} manual")
    print(f"farm: Auto verifying")
    try:
        # res = await (await aiorequests.post(url="http://pcrd.tencentbot.top/validate", data=dumps({"url": url}), headers=header)).content
        res = await (await aiorequests.get(url=url, headers=header)).content
        print(res)
        #if str(res.status_code) != "200":
        #    continue
        res = loads(res)
        uuid = res["uuid"]
        msg = [f"uuid={uuid}"]
        ccnt = 0
        while ccnt < 10 and succ == 0 and validate == "":
            ccnt += 1
            res = await (await aiorequests.get(url=f"https://pcrd.tencentbot.top/check/{uuid}")).content
            #if str(res.status_code) != "200":
            #    continue
            print(res)
            res = loads(res)
            if "queue_num" in res:
                nu = res["queue_num"]
                msg.append(f"queue_num={nu}")
                tim = min(int(nu), 3) * 20
                msg.append(f"sleep={tim}")
                #await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: \n" + "\n".join(msg))
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
                elif "validate" in info:
                    succ = 1
                    info = info["validate"]
            if ccnt >= 10:
                raise Exception("Captcha failed")
    except:
        raise
    if succ:
        validate = info
    #await bot.send_private_msg(user_id=acinfo['admin'], message=f"thread{ordd}: succ={succ} validate={validate}")
    print(f"farm: succ={succ} validate={validate}")

    # captcha_lck.release()
    # await captcha_lck.acquire()
    return validate
