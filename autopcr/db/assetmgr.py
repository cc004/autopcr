#type: ignore
from typing import List
from ..util import aiorequests
from ..util.logger import instance as logger
from ..constants import CACHE_DIR
import asyncio, os, pydantic
import UnityPy
from UnityPy.enums import ClassIDType
from .twasset import UNITYPY_LOCK
UnityPy.config.FALLBACK_UNITY_VERSION = "2021.3.20f1"


def _load_database(payload: bytes) -> bytes:
    with UNITYPY_LOCK:
        ab = UnityPy.load(payload)
        asset = ab.objects[0].read()
        script = getattr(
            asset,
            "m_Script",
            getattr(asset, "script", None),
        )
        if isinstance(script, str):
            return script.encode("utf-8", "surrogateescape")
        if script is not None:
            return bytes(script)
        raise ValueError("master TextAsset contains no script payload")


def _load_texture(payload: bytes):
    with UNITYPY_LOCK:
        ab = UnityPy.load(payload)
        for obj in ab.objects:
            if obj.type == ClassIDType.Texture2D:
                asset = obj.read()
                return asset.image
    return None

class content(pydantic.BaseModel):
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
        offset = len(splits) > 5
        return content(
            url=splits[0],
            md5=splits[1],
            type=splits[2 + offset],
            size=int(splits[3 + offset]),
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

        os.makedirs(os.path.join(CACHE_DIR, 'manifest'), exist_ok=True)
        cacheFile = os.path.join(CACHE_DIR, 'manifest', f'{ver}.json')
        try:
            self.root = content.parse_file(cacheFile)
            
            logger.info(f'manifest version {ver} loaded from cache')
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
        logger.info(f"resolving {url}...")
        
        content = self.registries[url]
        def genHash(hash):
            return f'{self.pool}/{content.category}/{hash[:2]}/{hash}'
        return await content.download(genHash)
 
    async def db(self) -> bytes:
        payload = await self.download('a/masterdata_master.unity3d')
        return await asyncio.get_running_loop().run_in_executor(
            None, _load_database, payload
        )

    async def unit_icon(self, unit_id: int) -> bytes:
        payload = await self.download(f'a/unit_icon_unit_{unit_id}.unity3d')
        return await asyncio.get_running_loop().run_in_executor(
            None, _load_texture, payload
        )

    async def ex_equip_icon(self, equip_id: int) -> bytes:
        payload = await self.download(f'a/icon_icon_extra_equip_{equip_id}.unity3d')
        return await asyncio.get_running_loop().run_in_executor(
            None, _load_texture, payload
        )


# should lock before use
instance = assetmgr()

