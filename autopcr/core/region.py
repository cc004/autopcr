from contextvars import ContextVar, Token


REGION_CN = "cn"
REGION_TW = "tw"

_current_region: ContextVar[str] = ContextVar(
    "autopcr_current_region", default=REGION_CN
)


def get_region() -> str:
    return _current_region.get()


def set_region(region: str) -> Token:
    if region not in (REGION_CN, REGION_TW):
        raise ValueError(f"Unsupported region: {region}")
    return _current_region.set(region)


def reset_region(token: Token) -> None:
    _current_region.reset(token)
