from autopcr.core import pcrclient, ApiException, sessionmgr
from autopcr.model.requests import *
from autopcr.model.responses import *
import autopcr.util.questutils as questutils

import asyncio

import os
import json

quests = [int(x) for x in '''
11001001
11001002
11001003
11001004
11001005
11001006
11001007
11001008
11001009
11001010
11002001
11002002
11002003
11002004
11002005
11002006
11002007
11002008
11002009
11002010
11002011
11002012
11003001
'''.strip().splitlines()]

import random

async def quest_pass(client: pcrclient, quest_id: int):
    if quest_id in client.data.quest_dict and client.data.quest_dict[quest_id].clear_flg:
        print(f'quest {quest_id} already passed')
        return
    print(f'passing quest: {quest_id}')

    await asyncio.sleep(2)

    token = questutils.create_quest_token()
    req = QuestStartRequest()
    req.token = token
    req.quest_id = quest_id
    req.support_unit_id = 0
    req.support_battle_rarity = 0
    req.owner_viewer_id = 0
    req.is_friend = 0
    resp = await client.request(req)

    await asyncio.sleep(5)

    req = QuestFinishRequest()
    req.fps = 60
    req.auto_clear = 0
    req.remain_time = 90000
    req.quest_id = quest_id
    req.unit_hp_list = []
    req.is_friend = 0
    req.owner_viewer_id = 0
    req.support_position = 0

    party = client.data.deck_list[ePartyType.QUEST]
    if party.unit_id1:
        info = UnitHpInfo(viewer_id=client.viewer_id, unit_id=party.unit_id1, hp = random.randint(10, 100))
        req.unit_hp_list.append(info)
    if party.unit_id2:
        info = UnitHpInfo(viewer_id=client.viewer_id, unit_id=party.unit_id2, hp = random.randint(10, 100))
        req.unit_hp_list.append(info)
    if party.unit_id3:
        info = UnitHpInfo(viewer_id=client.viewer_id, unit_id=party.unit_id3, hp = random.randint(10, 100))
        req.unit_hp_list.append(info)
    if party.unit_id4:
        info = UnitHpInfo(viewer_id=client.viewer_id, unit_id=party.unit_id4, hp = random.randint(10, 100))
        req.unit_hp_list.append(info)
    if party.unit_id5:
        info = UnitHpInfo(viewer_id=client.viewer_id, unit_id=party.unit_id5, hp = random.randint(10, 100))
        req.unit_hp_list.append(info)
    
    for enemy in resp.enemy_list:
        info = UnitHpInfo(viewer_id=0, unit_id=enemy.id, hp = 0)
        req.unit_hp_list.append(info)

    resp = await client.request(req)

async def main(client):
    await client.login()
    
    req = DeckUpdateRequest()
    req.deck_number = ePartyType.QUEST.value
    req.unit_id_1 = 100101
    req.unit_id_2 = 0
    req.unit_id_3 = 0
    req.unit_id_4 = 0
    req.unit_id_5 = 0
    await client.request(req)

    for quest_id in quests:
        while True:
            try:
                await quest_pass(client, quest_id)
                break
            except:
                await asyncio.sleep(10)
                pass

accounts = []

with open('farm_config.json', 'r') as fp:
    j = json.load(fp)
for acc in j['workers']:
    acc['account'] = acc['username']
    acc.pop('username')
    acc['platform'] = 2
    acc['channel'] = 1
    accounts.append(acc)

tasks = []

loop = asyncio.get_event_loop()

for acc in accounts:
    client = pcrclient(acc)
    tasks.append(loop.create_task(main(client)))

loop.run_forever()