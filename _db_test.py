from autopcr.db.assetmgr import instance as assetmgr
from autopcr.db.dbmgr import instance as dbmgr
from autopcr.db.database import db
import asyncio, collections
from autopcr.db.models import UnitDatum
from autopcr.core import datamgr

asyncio.run(assetmgr.init(202306151740))
asyncio.run(dbmgr.update_db(assetmgr))
db.update(dbmgr)

with dbmgr.session() as session:
    x = UnitDatum().query(session).first(lambda x: x.unit_id == 100101)

    print(x)