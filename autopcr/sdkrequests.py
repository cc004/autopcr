from typing import List
from .modelbase import *

class ToolSdkLoginResponse(ResponseBase):
    is_risk: bool = False
class ToolSdkLoginRequest(Request[ToolSdkLoginResponse]):
    uid: str = None
    access_key: str = None
    platform: str = None
    channel_id: str = None
    challenge: str = None
    validate: str = None
    seccode: str = None
    captcha_type: str = None
    image_token: str = None
    captcha_code: str = None
    @property
    def url(self) -> str:
        return "tool/sdk_login"

class CheckGameStartResponse(ResponseBase):
    now_tutorial: bool = False
class CheckGameStartRequest(Request[CheckGameStartResponse]):
    apptype: int = None
    campaign_data: str = None
    campaign_user: int = None
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
    json: int = None
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

