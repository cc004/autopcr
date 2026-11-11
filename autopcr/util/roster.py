import importlib

import pygtrie
import unicodedata
import zhconv

from . import pcr_data
from .logger import logging

def normalize_str(string) -> str:
    """
    规范化unicode字符串 并 转为小写 并 转为简体
    """
    string = unicodedata.normalize('NFKC', string)
    string = string.lower()
    string = zhconv.convert(string, 'zh-hans')
    return string

class Roster:

    def __init__(self):
        self._roster = pygtrie.CharTrie()
        self.update()

    def update(self):
        importlib.reload(pcr_data)
        self._roster.clear()
        for idx, names in pcr_data.CHARA_NAME.items():
            for n in names:
                n = normalize_str(n)
                if n not in self._roster:
                    self._roster[n] = idx
                else:
                    logging.warning(f'priconne.chara.Roster: 出现重名{n}于id{idx}与id{self._roster[n]}')

    def get_id(self, name):
        name = normalize_str(name)
        return self._roster[name] if name in self._roster else None

    def parse_team(self, namestr):
        """@return: List[ids], unknown_namestr"""
        namestr = normalize_str(namestr.strip())
        team = []
        unknown = []
        while namestr:
            item = self._roster.longest_prefix(namestr)
            if not item:
                unknown.append(namestr[0])
                namestr = namestr[1:].lstrip()
            else:
                team.append(item.value)
                namestr = namestr[len(item.key):].lstrip()
        return team, ''.join(unknown)

roster = Roster()
