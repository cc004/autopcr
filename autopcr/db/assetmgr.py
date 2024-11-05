#type: ignore
from typing import List, Callable
from ..util import aiorequests
from ..constants import CACHE_DIR
import os
from pydantic.v1 import BaseModel
import UnityPy

class content(BaseModel):
    url: str = None
    md5: str = None
    type: str = None
    category: str = None
    size: int = 0
    children: List["content"] = None

    @property
    def is_assets(self) -> bool:
        return not self.url.startswith('manifest/')

    @staticmethod
    def from_line(line: str, category: str) -> "content":
        splits = line.split(',')
        return content(
            url=splits[0],
            md5=splits[1],
            type=splits[2],
            size=int(splits[3]),
            category=category,
            children=[]
        )
    
    @staticmethod
    async def from_url(urlroot: str, url: str, category: str) -> List["content"]:
        lines = (await (await aiorequests.get(f'{urlroot}{url}')).text).split('\n')
        res = [content.from_line(line, category) for line in lines]
        for child in res:
            await child.download_children(urlroot)
        return res

    async def download_children(self, urlroot: str):
        if not self.is_assets:
            self.children = await content.from_url(urlroot, self.url, self.category)

    def register_to(self, mgr: "assetmgr"):
        mgr.registries[self.url] = self
        for child in self.children:
            child.register_to(mgr)
        
    async def download(self, urlgetter) -> bytes:
        return await (await aiorequests.get(urlgetter(self.md5))).content

class assetmgr:
    def __init__(self):
        self.ver = None
        self.root = None
        self.registries: dict[str, content] = {}

    res = 'https://l1-prod-patch-gzlj.bilibiligame.net/client_ob_771'

    @property
    def manifest(self) -> str:
        return f'{self.res}/Manifest'
    
    @property
    def pool(self) -> str:
        return f'{self.res}/pool'

    async def init(self, ver):
        self.registries.clear()

        cacheFile = os.path.join(CACHE_DIR, 'manifest', f'{ver}.json')
        try:
            self.root = content.parse_file(cacheFile)
            
            print(f'manifest version {ver} loaded from cache')
        except:
            self.root = content(
                url='manifest/manifest_assetmanifest',
                type='every',
                category='AssetBundles/Android',
                children=await content.from_url(f'{self.manifest}/AssetBundles/Android/{ver}/', 'manifest/manifest_assetmanifest', 'AssetBundles/Android')
            )
            with open(cacheFile, 'w') as f:
                f.write(self.root.json())

        self.ver = ver
        self.root.register_to(self)

    async def download(self, url: str) -> bytes:
        content = self.registries[url]
        def genHash(hash):
            return f'{self.pool}/{content.category}/{hash[:2]}/{hash}'
        return await content.download(genHash)
 
    async def db(self) -> bytes:
        ab = UnityPy.load(await self.download('a/masterdata_master.unity3d'))
        asset = ab.objects[0].read()
        return asset.script


# should lock before use
instance = assetmgr()
