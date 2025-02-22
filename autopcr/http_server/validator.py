from typing import Dict, List
from ..util import questutils
from ..model.error import PanicError
import asyncio
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import defaultdict
from ..sdk.validator import remoteValidator, localValidator
from ..sdk.bsgamesdk import captch
from ..util.logger import instance as logger

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
    async def validator():
        return await Validator(qq)
    return validator

async def Validator(qq):
    info = None
    for validator in [remoteValidator, localValidator, lambda: manualValidator(qq)]:
        try:
            info = await validator()
            if info:
                break
        except Exception as e:
            logger.exception(e)
    if not info:
        raise PanicError("验证码验证超时")
    return info

async def manualValidator(qq):

    if not manual_validator_enabled:
        raise PanicError("manual validator disabled")

    logger.info('use manual validator')

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
            account_aenter_legacy = result.__aenter__
            async def account_aenter():
                res = await account_aenter_legacy()
                if not res.readonly:
                    res.client.session.sdk.append_post_login(post_login)
                    res.client.session.sdk.captchaVerifier = create_validator(qid)
                return res
            
            result.__aenter__ = account_aenter
            return result
        result.load = accountmgr_load
        return result
    usermgr.load = usermgr_load
