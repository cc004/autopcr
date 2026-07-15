#type: ignore
from typing import List, Optional
from .modelbase import *
from pydantic import Field

class ToolSdkLoginResponse(ResponseBase):
    is_risk: bool = False
class ToolSdkLoginRequest(Request[ToolSdkLoginResponse]):
    uid: str = None
    access_key: str = None
    platform: str = None
    channel_id: str = None
    challenge: str = None
    validate_: Optional[str] = Field(alias='validate')
    seccode: str = None
    captcha_type: str = None
    image_token: str = None
    captcha_code: str = None
    @property
    def url(self) -> str:
        return "tool/sdk_login"

class CheckGameStartResponse(ResponseBase):
    now_tutorial: bool = False
    bundle_ver: str = None
class CheckGameStartRequest(Request[CheckGameStartResponse]):
    apptype: int = None
    campaign_data: str = None
    campaign_user: int = None
    @property
    def url(self) -> str:
        return "check/game_start"

class TwCheckGameStartRequest(Request[CheckGameStartResponse]):
    # TW 5.7.0's Cute.GameStartCheckTask.CheckParams schema.  TW login leaves
    # these business fields unset: the server accepts the transport-only
    # payload, and fabricating attribution/anti-tamper values is less faithful
    # than omitting them.
    app_type: int = None
    campaign_data: str = None
    campaign_sign: str = None
    campaign_user: int = None
    adid: str = None
    endpointArn: str = None
    countrycode: str = None
    FOXYOROKOBINODANCE: str = None
    FOXYOROKOBINOMAI: str = None
    @property
    def url(self) -> str:
        return "check/game_start"

class SourceIniIndexResponse(ResponseBase):
    server: List[str] = None
class SourceIniIndexRequest(Request[SourceIniIndexResponse]):
    @property
    def url(self) -> str:
        return "source_ini/index?format=json"
    @property
    def crypted(self) -> bool:
        return False

class SourceIniGetMaintenanceStatusResponse(ResponseBase):
    _json: int = Field(alias='json')
    encrypt: int = None
    res_http_type: int = None
    node_type: int = None
    silence_download_size: int = None
    res_ver: str = None
    execl_ver: str = None
    res_key: str = None
    start_time: str = None
    manifest_ver: str = None
    required_manifest_ver: str = None
    movie_ver: str = None
    sound_ver: str = None
    patch_ver: str = None
    resource: List[str] = None
    maintenance_message: str = None
class SourceIniGetMaintenanceStatusRequest(Request[SourceIniGetMaintenanceStatusResponse]):
    @property
    def url(self) -> str:
        return "source_ini/get_maintenance_status?format=json"
    @property
    def crypted(self) -> bool:
        return False

