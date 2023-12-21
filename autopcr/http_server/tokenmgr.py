import secrets
import datetime
from typing import Tuple, Union

class OneTimeToken:
    def __init__(self, expiration_minutes=1, qid: str = ""):
        self.token = secrets.token_urlsafe(16)
        self.expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=expiration_minutes)
        self.qid = qid

    def is_valid(self):
        return self.qid and datetime.datetime.now() < self.expiration_time

class Tokenmgr:

    def __init__(self, expiration_time = 1):
        self.token_pool = {}
        self.expiration_time = expiration_time

    def generate_token(self, qid: str = "") -> str:
        token = OneTimeToken(self.expiration_time, qid)
        self.token_pool[token.token] = token
        return token.token

    def set_qid(self, token: str, qid: str) -> bool:
        if token in self.token_pool:
            self.token_pool[token].qid = qid
            return True
        return False

    def validate_token(self, token: str) -> Tuple[bool, str]:
        ok = False
        qid = ""
        if token in self.token_pool:
            ok = self.token_pool[token].is_valid()
            qid = self.token_pool[token].qid
            del self.token_pool[token]
        return ok, qid

instance = Tokenmgr()
