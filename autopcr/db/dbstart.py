import glob, os
from ..constants import CACHE_DIR
from ..core.datamgr import datamgr
from ..util import aiorequests
import brotli

async def db_start():
    dbs = glob.glob(os.path.join(CACHE_DIR, "db", "*.db"))
    if dbs:
        db = max(dbs)
        version = int(os.path.basename(db).split('.')[0])
    else:
        version = await do_update_database()
    await datamgr.try_update_database(version)

async def do_update_database() -> int:
    info = f'https://redive.estertion.win/last_version_cn.json'

    rsp = await aiorequests.get(info, stream=True, timeout=20)
    version = (await rsp.json())['TruthVersion']

    url = f'https://redive.estertion.win/db/redive_cn.db.br'

    os.makedirs(os.path.join(CACHE_DIR, 'db'), exist_ok=True)
    save_path = os.path.join(CACHE_DIR, "db", f"{version}.db")
    try:
        rsp = await aiorequests.get(url, headers={'Accept-Encoding': 'br'}, stream=True, timeout=20)
        if 200 == rsp.status_code:
            with open(save_path, "wb") as f:
                f.write(brotli.decompress((await rsp.content)))
        else:
            raise ValueError("下载失败")
    except Exception as e:
        raise e
    return int(version)
