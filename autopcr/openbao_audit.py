import json
import logging
import os
from dataclasses import dataclass
from logging.handlers import TimedRotatingFileHandler

from .constants import AUDIT_DIR

AUDIT_LOG_PATH = os.path.join(AUDIT_DIR, "autopcr-openbao.log")


@dataclass(frozen=True)
class OpenBaoAuditContext:
    qq: str
    display_name: str


class _PrivateTimedRotatingFileHandler(TimedRotatingFileHandler):
    def _open(self):
        stream = super()._open()
        os.chmod(self.baseFilename, 0o600)
        return stream


def _create_logger():
    os.makedirs(AUDIT_DIR, mode=0o700, exist_ok=True)
    os.chmod(AUDIT_DIR, 0o700)

    audit_logger = logging.getLogger("autopcr.openbao.audit")
    audit_logger.setLevel(logging.INFO)
    audit_logger.propagate = False
    if not any(
        isinstance(handler, _PrivateTimedRotatingFileHandler)
        for handler in audit_logger.handlers
    ):
        handler = _PrivateTimedRotatingFileHandler(
            AUDIT_LOG_PATH,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        handler.suffix = "%Y-%m-%d.log"
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        audit_logger.addHandler(handler)
    return audit_logger


_logger = _create_logger()


def record(event, **details):
    _logger.info(
        "%s",
        json.dumps(
            {"event": event, **details},
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ),
    )
