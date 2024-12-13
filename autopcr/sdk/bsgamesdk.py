import json
import time
import hashlib
from . import rsacr
import urllib
from ..util import aiorequests

bililogin="https://line1-sdk-center-login-sh.biligame.net/"

async def sendpost(url,data):
    header ={
        "User-Agent": "Mozilla/5.0 BSGameSDK",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "line1-sdk-center-login-sh.biligame.net"
    }
    res = await (await aiorequests.post(url=url,data=data,headers=header)).content
    return json.loads(res)

def setsign(data):
    data["timestamp"]=int(time.time())
    data["client_timestamp"]=int(time.time())
    sign=""
    data2=""
    for key in data:
        if key=="pwd":
            pwd=urllib.parse.quote(data["pwd"])
            data2+=f"{key}={pwd}&"
        data2+=f"{key}={data[key]}&"
    for key in sorted(data):
        sign+=f"{data[key]}"
    data=sign
    sign=sign+"fe8aac4e02f845b8ad67c427d48bfaf1"
    sign=hashlib.md5(sign.encode()).hexdigest()
    data2+="sign="+sign
    return data2
modolrsa='{"operators":"5","merchant_id":"1","isRoot":"0","domain_switch_count":"0","sdk_type":"1","sdk_log_type":"1","timestamp":"1613035485639","support_abis":"x86,armeabi-v7a,armeabi","access_key":"","sdk_ver":"3.4.2","oaid":"","dp":"1280*720","original_domain":"","imei":"227656364311444","version":"1","udid":"KREhESMUIhUjFnJKNko2TDQFYlZkB3cdeQ==","apk_sign":"e89b158e4bcf988ebd09eb83f5378e87","platform_type":"3","old_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","android_id":"84567e2dda72d1d4","fingerprint":"","mac":"08:00:27:53:DD:12","server_id":"1592","domain":"line1-sdk-center-login-sh.biligame.net","app_id":"1370","version_code":"90","net":"4","pf_ver":"6.0.1","cur_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","c":"1","brand":"Android","client_timestamp":"1613035486888","channel_id":"1","uid":"","game_id":"1370","ver":"2.4.10","model":"MuMu"}'
modollogin='{"operators":"5","merchant_id":"1","isRoot":"0","domain_switch_count":"0","sdk_type":"1","sdk_log_type":"1","timestamp":"1613035508188","support_abis":"x86,armeabi-v7a,armeabi","access_key":"","sdk_ver":"3.4.2","oaid":"","dp":"1280*720","original_domain":"","imei":"227656364311444","gt_user_id":"fac83ce4326d47e1ac277a4d552bd2af","seccode":"","version":"1","udid":"KREhESMUIhUjFnJKNko2TDQFYlZkB3cdeQ==","apk_sign":"e89b158e4bcf988ebd09eb83f5378e87","platform_type":"3","old_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","android_id":"84567e2dda72d1d4","fingerprint":"","validate":"84ec07cff0d9c30acb9fe46b8745e8df","mac":"08:00:27:53:DD:12","server_id":"1592","domain":"line1-sdk-center-login-sh.biligame.net","app_id":"1370","pwd":"rxwA8J+GcVdqa3qlvXFppusRg4Ss83tH6HqxcciVsTdwxSpsoz2WuAFFGgQKWM1+GtFovrLkpeMieEwOmQdzvDiLTtHeQNBOiqHDfJEKtLj7h1nvKZ1Op6vOgs6hxM6fPqFGQC2ncbAR5NNkESpSWeYTO4IT58ZIJcC0DdWQqh4=","version_code":"90","net":"4","pf_ver":"6.0.1","cur_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","c":"1","brand":"Android","client_timestamp":"1613035509437","channel_id":"1","uid":"","captcha_type":"1","game_id":"1370","challenge":"efc825eaaef2405c954a91ad9faf29a2","user_id":"doo349","ver":"2.4.10","model":"MuMu"}'
modolcaptch='{"operators":"5","merchant_id":"1","isRoot":"0","domain_switch_count":"0","sdk_type":"1","sdk_log_type":"1","timestamp":"1613035486182","support_abis":"x86,armeabi-v7a,armeabi","access_key":"","sdk_ver":"3.4.2","oaid":"","dp":"1280*720","original_domain":"","imei":"227656364311444","version":"1","udid":"KREhESMUIhUjFnJKNko2TDQFYlZkB3cdeQ==","apk_sign":"e89b158e4bcf988ebd09eb83f5378e87","platform_type":"3","old_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","android_id":"84567e2dda72d1d4","fingerprint":"","mac":"08:00:27:53:DD:12","server_id":"1592","domain":"line1-sdk-center-login-sh.biligame.net","app_id":"1370","version_code":"90","net":"4","pf_ver":"6.0.1","cur_buvid":"XZA2FA4AC240F665E2F27F603ABF98C615C29","c":"1","brand":"Android","client_timestamp":"1613035487431","channel_id":"1","uid":"","game_id":"1370","ver":"2.4.10","model":"MuMu"}'
async def login1(account,password):
    data=json.loads(modolrsa)
    data=setsign(data)
    rsa=await sendpost(bililogin+"api/client/rsa",data)
    data=json.loads(modollogin)
    public_key=rsa['rsa_key']
    data["access_key"]=""
    data["gt_user_id"]=""
    data["uid"]=""
    data["challenge"]=""
    data["user_id"]=account
    data["validate"]=""
    data["pwd"]=rsacr.rsacreate(rsa['hash']+password,public_key)
    data=setsign(data).encode("utf-8")
    return await sendpost(bililogin+"api/client/login",data)
async def login2(account,password,challenge,gt_user,validate):
    data=json.loads(modolrsa)
    data=setsign(data)
    rsa=await sendpost(bililogin+"api/client/rsa",data)
    data=json.loads(modollogin)
    public_key=rsa['rsa_key']
    data["access_key"]=""
    data["gt_user_id"]=gt_user
    data["uid"]=""
    data["challenge"]=challenge
    data["user_id"]=account
    data["validate"]=validate
    data["seccode"]=validate+"|jordan"
    data["pwd"]=rsacr.rsacreate(rsa['hash']+password,public_key)
    data=setsign(data).encode("utf-8")
    return await sendpost(bililogin+"api/client/login",data)
async def captch():
    data=json.loads(modolcaptch)
    data=setsign(data)
    return await sendpost(bililogin+"api/client/start_captcha",data)
    '''
def make_captch(gt,challenge,gt_user):
    data={}
    data['username']=""
    data['appkey']=""
    data['gt']=gt
    data['challenge']=challenge
    capurl=f"https://game.bilibili.com/sdk/geetest/?captcha_type=1&challenge={challenge}&gt={gt}&userid={gt_user}&gs=1"
    print(capurl)
    data['referer']=urllib.parse.quote(capurl)
    data['handle_method']="three_on"
    print(data)
    res = requests.get(url="http://api.ydaaa.com/start_handle",params=data)
    return res
    '''
async def login(bili_account,bili_pwd, make_captch):
    print(f'logging in with acc={bili_account}, pwd = {bili_pwd}')
    login_sta= await login1(bili_account,bili_pwd)
    # if "access_key" not in login_sta:
    if login_sta['code'] == 200000:
        captch_done=await make_captch()
        login_sta=await login2(bili_account,bili_pwd,captch_done["challenge"],captch_done['gt_user_id'],captch_done['validate'])
        return login_sta
    else:
        return login_sta
'''
def getcap():
    cap=captch()
    print(cap.text)
    cap=json.loads(cap.text)
    capurl=f"https://help.tencentbot.top/geetest/?captcha_type=1&challenge={cap['challenge']}&gt={cap['gt']}&userid={cap['gt_user_id']}&gs=1"
    return capurl
'''
