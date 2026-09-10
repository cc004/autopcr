import asyncio
import json
import os
from typing import Dict, Set, Tuple

import msgpack
import UnityPy
from UnityPy.enums import ClassIDType

from ..constants import CACHE_DIR
from ..util import aiorequests
from ..util.logger import instance as logger

UnityPy.config.FALLBACK_UNITY_VERSION = "2021.3.20f1"

AssetEntry = Tuple[str, str]
AssetRegistry = Dict[str, AssetEntry]

COMPACT_MANIFEST_FORMAT = 1
MANIFEST_CATEGORY = "AssetBundles/Android"
ROOT_MANIFEST = "manifest/manifest_assetmanifest"


class assetmgr:
    def __init__(self):
        self.ver = None
        self._loaded_ver = None
        self.registries: AssetRegistry = {}
        self._manifest_lock = asyncio.Lock()

    res = 'https://l1-prod-patch-gzlj.bilibiligame.net/client_ob_771'

    @property
    def manifest(self) -> str:
        return f'{self.res}/Manifest'

    @property
    def pool(self) -> str:
        return f'{self.res}/pool'

    @staticmethod
    def _manifest_dir() -> str:
        return os.path.join(CACHE_DIR, 'manifest')

    @classmethod
    def _compact_cache_path(cls, ver: int) -> str:
        return os.path.join(cls._manifest_dir(), f'{ver}.compact.msgpack')

    @classmethod
    def _legacy_cache_path(cls, ver: int) -> str:
        return os.path.join(cls._manifest_dir(), f'{ver}.json')

    @staticmethod
    def _validate_registry(raw_assets, ver: int) -> AssetRegistry:
        # 紧凑格式按 category 分组存储，避免同一 category 字符串在每个条目里重复一遍
        if not isinstance(raw_assets, dict):
            raise ValueError(f'compact manifest {ver} assets must be a map')

        registry: AssetRegistry = {}
        for category, urls in raw_assets.items():
            if not isinstance(category, str) or not category:
                raise ValueError(f'compact manifest {ver} contains an invalid category')
            if not isinstance(urls, dict):
                raise ValueError(f'compact manifest {ver} assets for {category} must be a map')
            for url, md5 in urls.items():
                if not isinstance(url, str) or not url:
                    raise ValueError(f'compact manifest {ver} contains an invalid URL')
                if not isinstance(md5, str) or not md5:
                    raise ValueError(f'compact manifest {ver} contains an invalid md5 for {url}')
                registry[url] = (md5, category)

        if not registry:
            raise ValueError(f'compact manifest {ver} contains no assets')
        return registry

    @classmethod
    def _load_compact_cache(cls, path: str, ver: int) -> AssetRegistry:
        with open(path, 'rb') as f:
            payload = msgpack.unpackb(f.read(), raw=False)

        if not isinstance(payload, dict):
            raise ValueError(f'compact manifest {ver} must be a map')
        if payload.get('format') != COMPACT_MANIFEST_FORMAT:
            raise ValueError(f'unsupported compact manifest format for version {ver}')
        if payload.get('version') != ver:
            raise ValueError(f'compact manifest version mismatch: expected {ver}')
        return cls._validate_registry(payload.get('assets'), ver)

    @classmethod
    def _load_legacy_cache(cls, path: str, ver: int) -> AssetRegistry:
        with open(path, 'r', encoding='utf-8') as f:
            root = json.load(f)

        # 同一 URL 会同时出现在 xxx_assetmanifest 与后继的 xxx_assetmanifest_s 中，
        # 只有后者的 hash 在 pool 里真实存在，因此必须按先序遍历让后出现的条目覆盖前者
        registry: AssetRegistry = {}
        stack = [root]
        while stack:
            node = stack.pop()
            if not isinstance(node, dict):
                raise ValueError(f'legacy manifest {ver} contains a non-object node')

            children = node.get('children') or []
            if not isinstance(children, list):
                raise ValueError(f'legacy manifest {ver} contains invalid children')
            stack.extend(reversed(children))

            url = node.get('url')
            if not isinstance(url, str) or not url or url.startswith('manifest/'):
                continue
            md5 = node.get('md5')
            category = node.get('category')
            if not isinstance(md5, str) or not md5:
                raise ValueError(f'legacy manifest {ver} contains an invalid md5 for {url}')
            if not isinstance(category, str) or not category:
                raise ValueError(f'legacy manifest {ver} contains an invalid category for {url}')
            registry[url] = (md5, category)

        if not registry:
            raise ValueError(f'legacy manifest {ver} contains no assets')
        return registry

    @classmethod
    def _write_compact_cache(cls, path: str, ver: int, registry: AssetRegistry):
        assets: Dict[str, Dict[str, str]] = {}
        for url, (md5, category) in registry.items():
            assets.setdefault(category, {})[url] = md5
        payload = {
            'format': COMPACT_MANIFEST_FORMAT,
            'version': ver,
            'assets': assets,
        }
        data = msgpack.packb(payload, use_bin_type=True)
        temporary_path = f'{path}.{os.getpid()}.tmp'
        try:
            with open(temporary_path, 'wb') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporary_path, path)
        finally:
            if os.path.exists(temporary_path):
                os.remove(temporary_path)

    async def _fetch_manifest(
        self,
        urlroot: str,
        manifest_url: str,
        category: str,
        registry: AssetRegistry,
        visited: Set[str],
    ):
        if manifest_url in visited:
            return
        visited.add(manifest_url)

        response = await aiorequests.get(f'{urlroot}{manifest_url}')
        lines = (await response.text).splitlines()
        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue
            fields = line.split(',')
            if len(fields) < 4:
                raise ValueError(f'invalid manifest line {manifest_url}:{line_number}')

            url, md5 = fields[0], fields[1]
            if not url:
                raise ValueError(f'empty asset URL at {manifest_url}:{line_number}')
            if url.startswith('manifest/'):
                await self._fetch_manifest(urlroot, url, category, registry, visited)
            else:
                if not md5:
                    raise ValueError(f'empty asset md5 at {manifest_url}:{line_number}')
                registry[url] = (md5, category)

    async def _fetch_registry(self, ver: int) -> AssetRegistry:
        registry: AssetRegistry = {}
        urlroot = f'{self.manifest}/{MANIFEST_CATEGORY}/{ver}/'
        await self._fetch_manifest(
            urlroot,
            ROOT_MANIFEST,
            MANIFEST_CATEGORY,
            registry,
            set(),
        )
        if not registry:
            raise ValueError(f'remote manifest {ver} contains no assets')
        return registry

    async def _load_registry(self, ver: int) -> AssetRegistry:
        os.makedirs(self._manifest_dir(), exist_ok=True)
        compact_path = self._compact_cache_path(ver)
        legacy_path = self._legacy_cache_path(ver)
        registry = None

        try:
            registry = self._load_compact_cache(compact_path, ver)
            logger.info(f'compact manifest version {ver} loaded from cache')
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError, msgpack.ExtraData, msgpack.FormatError, msgpack.StackError) as e:
            logger.warning(f'failed to load compact manifest version {ver}: {e}')

        if registry is None:
            try:
                registry = self._load_legacy_cache(legacy_path, ver)
                logger.info(f'legacy manifest version {ver} loaded from cache')
            except FileNotFoundError:
                pass
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as e:
                logger.warning(f'failed to load legacy manifest version {ver}: {e}')

            if registry is None:
                registry = await self._fetch_registry(ver)
                logger.info(f'manifest version {ver} loaded from remote')

            # registry 已在内存可用，缓存写失败（如磁盘满）不应阻断本次加载
            try:
                self._write_compact_cache(compact_path, ver, registry)
            except OSError as e:
                logger.warning(f'failed to write compact manifest version {ver}: {e}')

        return registry

    def set_version(self, ver: int):
        self.ver = ver

    async def _ensure_loaded_locked(self, ver: int):
        if self._loaded_ver == ver:
            return

        registry = await self._load_registry(ver)
        self.registries = registry
        self._loaded_ver = ver

    async def ensure_loaded(self, ver=None):
        target_ver = self.ver if ver is None else ver
        if target_ver is None:
            raise RuntimeError('asset manifest version is not set')

        # 稳态无锁快路径：其原子性依赖"此检查与调用方读取 registries 之间没有 await 点"，
        # registries 与 _loaded_ver 在 _ensure_loaded_locked 中也是无挂起点地成对更新
        if self._loaded_ver == target_ver:
            return

        # 在锁内重取版本号，避免等锁期间版本切换导致按旧版本多做一次重载
        async with self._manifest_lock:
            target_ver = self.ver if ver is None else ver
            await self._ensure_loaded_locked(target_ver)

    async def init(self, ver):
        self.set_version(ver)
        await self.ensure_loaded(ver)

    async def _resolve_asset(self, url: str) -> AssetEntry:
        await self.ensure_loaded()
        return self.registries[url]

    async def download(self, url: str) -> bytes:
        logger.info(f"resolving {url}...")

        md5, category = await self._resolve_asset(url)
        download_url = f'{self.pool}/{category}/{md5[:2]}/{md5}'
        return await (await aiorequests.get(download_url)).content

    async def db(self) -> bytes:
        ab = UnityPy.load(await self.download('a/masterdata_master.unity3d'))
        asset = ab.objects[0].read()
        return asset.script

    async def unit_icon(self, unit_id: int) -> bytes:
        ab = UnityPy.load(await self.download(f'a/unit_icon_unit_{unit_id}.unity3d'))
        for object in ab.objects:
            if object.type == ClassIDType.Texture2D:
                asset = object.read()
                return asset.image
        return None

    async def ex_equip_icon(self, equip_id: int) -> bytes:
        ab = UnityPy.load(await self.download(f'a/icon_icon_extra_equip_{equip_id}.unity3d'))
        for object in ab.objects:
            if object.type == ClassIDType.Texture2D:
                asset = object.read()
                return asset.image
        return None


# should lock before use
instance = assetmgr()