from autopcr.core import pcrclient, ApiException, sessionmgr
from autopcr.model.requests import *
from autopcr.model.responses import *
import asyncio

accounts = []

import os
import json

try:
    dismissed = json.load(open('dismissed.json', 'r'))
except:
    dismissed = []

dismissed = set(dismissed)

with open('farm_config.json', 'r') as fp:
    j = json.load(fp)
for acc in j['workers']:
    acc['account'] = acc['username']
    acc.pop('username')
    acc['platform'] = 2
    acc['channel'] = 1
    accounts.append(acc)

SEARCH_START = 0
SEARCH_END = 2000000

ids = [x for x in range(SEARCH_START, SEARCH_END) if x not in dismissed]

id_lck = asyncio.Lock()

dismissed_t = []

dismissed_lck = asyncio.Lock()

current = 0

import datetime

date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fout = open(f'clan_{date}.log', 'w')

fout_lck = asyncio.Lock()

last_ok = -1

run_once = False
run_once_lck = asyncio.Lock()

async def run_once_saveall():
    global dismissed, dismissed_t, last_ok, run_once
    async with run_once_lck:
        if run_once:
            return
        run_once = True
    async with dismissed_lck:
        dismissed += [
            x for x in dismissed_t if x < last_ok
        ]
        json.dump(dismissed, open('dismissed.json', 'w'))
    
    fout.close()

async def worker(account):
    global current, last_ok
    client = pcrclient(account)
    
    for comp in client._components:
        if type(comp) is sessionmgr:
            comp: sessionmgr
            comp.auto_relogin = False

    await client.login()

   # print((await client.get_hatsune_top(client.data.event_statuses[0].event_id)).json())
   # exit(0)
    while True:
        async with id_lck:
            id = ids[current]
            current += 1
            if id > last_ok + 10000: # 1w个都没成功，认为已经无法成功
                await run_once_saveall()
                break
        while True:
            req = OtherClanInfoRequest()
            req.clan_id = id
            try:
                resp = await client.request(req)
                async with fout_lck:
                    last_ok = max(last_ok, id)
                    fout.write(f'{resp.json()}\n')
                print(f'[{id}] {resp.clan.detail.clan_name}')
                break
            except ApiException as ex:
                if '此行会已解散。' in ex.args[0]:
                    async with dismissed_lck:
                        dismissed_t.append(id)
                    print(f'[{id}]{ex}')
                    break

                print(f'[{id}]{ex}')
                for comp in client._components:
                    if type(comp) is sessionmgr:
                        comp: sessionmgr
                        comp._logged = False
                await client.login()

import asyncio

main = asyncio.gather(*[worker(x) for x in accounts])

asyncio.get_event_loop().run_forever()