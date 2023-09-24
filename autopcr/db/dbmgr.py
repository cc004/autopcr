from ..constants import CACHE_DIR
from .assetmgr import assetmgr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

class dbmgr:
    def __init__(self):
        self.ver = None
        self._dbpath = None
        self._engine = None

    async def update_db(self, mgr: assetmgr):
        self.ver = mgr.ver
        self._dbpath = os.path.join(CACHE_DIR, 'db', f'{self.ver}.db')
        if not os.path.exists(self._dbpath):
            data = await mgr.db()
            with open(self._dbpath, 'wb') as f:
                f.write(data)
            print(f'db version {self.ver} updated')
        self._engine = create_engine(f'sqlite:///{self._dbpath}')
    
    def session(self) -> Session:
        return Session(self._engine)
        
instance = dbmgr()