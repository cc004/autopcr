from typing import Dict, List
from ..util import questutils
from ..model.error import PanicError
from json import loads
import asyncio, time
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import defaultdict
from ..sdk.validator import remoteValidator, localValidator
from ..core.sdkclient import sdkclient
from ..sdk.bsgamesdk import captch

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

def create_validator(qq):
    async def validator(client: sdkclient):
        return await Validator(qq, client)
    return validator

async def Validator(qq, client: sdkclient):
    info = None
    for validator in [remoteValidator, localValidator, lambda x: manualValidator(qq, x)]:
        try:
            info = await validator(client)
            if info:
                break
        except Exception as e:
            import traceback
            traceback.print_exc()
            pass
    if not info:
        raise PanicError("验证码验证超时")
    return info

async def manualValidator(qq, client: sdkclient):

    if not manual_validator_enabled:
        raise PanicError("manual validator disabled")

    print('use manual validator')

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

manual_validator_enabled = False

def enable_manual_validator():
    global manual_validator_enabled
    if manual_validator_enabled:
        return
    manual_validator_enabled = True

    from ..module.accountmgr import instance as usermgr
    usermgr_load_legacy = usermgr.load
    def usermgr_load(qid: str, readonly=False):
        result = usermgr_load_legacy(qid, readonly=readonly)
        accountmgr_load_legacy = result.load
        def accountmgr_load(account: str = "", readonly=False):
            result = accountmgr_load_legacy(account=account, readonly=readonly)
            
            async def post_login():
                validate_dict[qid].append(ValidateInfo(status="ok"))
            result.client.session.sdk.post_login = post_login
            result.client.session.sdk.captchaVerifier = create_validator(qid)

            return result
        result.load = accountmgr_load
        return result
    usermgr.load = usermgr_load