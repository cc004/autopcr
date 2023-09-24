import os, json
from ..util.linq import flow
from ..constants import DATA_DIR
from collections import Counter
from typing import Dict, Counter as TCounter
from ..model.common import eInventoryType
from ..model.custom import ItemType


def read_from(filename: str) -> object:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


extra_drops: Dict[int, TCounter[ItemType]] = (
    flow(read_from(os.path.join(DATA_DIR, 'extraDrops.json')))
    .select(lambda x: (
        x['questId'] // 1000,
        flow(x['dropItems'])
        .select(lambda y: (eInventoryType.Equip, y['id']))
        .to_list(),
        2 if x['questLevel'] >= 48 else 1,  # slot num
    ))
    .select(lambda x: (
        x[0],  # questId
        x[1],  # item
        x[2] / len(x[1]),  # prob
    ))
    .to_dict(lambda x: x[0], lambda x: Counter(
        flow(x[1]).to_dict(
            lambda y: y,
            lambda _: x[2]
        )
    ))
)
