import asyncio
import glob
import os
import sqlite3
import time
import uuid

import aiohttp
import brotli

from ..constants import CACHE_DIR, DATA_DIR
from ..core.apiclient import apiclient
from ..core.datamgr import datamgr
from ..core.sdkclient import account, platform
from ..core.region import REGION_CN, REGION_TW
from ..model.sdkrequests import SourceIniGetMaintenanceStatusRequest
from ..sdk.sdkclients import bsdkclient
from ..util.logger import instance as logger
from .database import db
from .dbmgr import dbmgr, get_dbmgr
from .twasset import (
    TW_ROOT_MANIFEST,
    find_tw_master_bundle,
    find_tw_master_manifests,
    normalize_tw_resource_version,
    parse_tw_manifest,
    tw_bundle_url,
    tw_manifest_url,
    validate_tw_resource,
    extract_tw_master_database,
)


_database_locks = {
    REGION_CN: asyncio.Lock(),
    REGION_TW: asyncio.Lock(),
}
_database_checked_at = {
    REGION_CN: 0.0,
    REGION_TW: 0.0,
}
_database_resource_versions = {
    REGION_TW: None,
}

TW_VERSION_URL = (
    'https://raw.githubusercontent.com/Expugn/'
    'priconne-database/master/version.json'
)
TW_DATABASE_URL = (
    'https://raw.githubusercontent.com/Expugn/'
    'priconne-database/master/master_tw.db'
)
TW_REQUIRED_TABLES = (
    'campaign_schedule',
    'equipment_data',
    'hatsune_schedule',
    'quest_data',
    'story_detail',
    'unit_data',
)
TW_MAX_MANIFEST_SIZE = 4 * 1024 * 1024
TW_MAX_MASTER_BUNDLE_SIZE = 128 * 1024 * 1024
TW_MAX_MIRROR_DATABASE_SIZE = 128 * 1024 * 1024


def _db_dir(region: str) -> str:
    if region == REGION_CN:
        # Preserve the existing CN cache layout.
        return os.path.join(CACHE_DIR, 'db')
    return os.path.join(CACHE_DIR, 'db', region)


def _cached_databases(region: str):
    pattern = (
        os.path.join(_db_dir(region), '**', '*.db')
        if region == REGION_TW
        else os.path.join(_db_dir(region), '*.db')
    )
    return glob.glob(pattern, recursive=region == REGION_TW)


def _tw_database_path(
    source: str,
    version: int,
    identity: str = None,
) -> str:
    if source not in {'official', 'mirror'}:
        raise ValueError(f'Unsupported TW database source: {source}')
    suffix = ''
    if identity:
        identity = str(identity).strip().lower()
        if source != 'mirror':
            raise ValueError('Only TW mirror caches accept an identity')
        if (
            not 8 <= len(identity) <= 128
            or any(ch not in '0123456789abcdef' for ch in identity)
        ):
            raise ValueError('Invalid TW mirror cache identity')
        suffix = f'-{identity}'
    return os.path.join(
        _db_dir(REGION_TW), source, f'{int(version):08d}{suffix}.db'
    )


def _legacy_tw_database_path(version: int) -> str:
    return os.path.join(_db_dir(REGION_TW), f'{int(version):08d}.db')


def _version_from_path(path: str) -> int:
    stem = os.path.splitext(os.path.basename(path))[0]
    return int(stem.split('-', 1)[0])


def _valid_tw_cache(path: str) -> bool:
    """Cheap structural check before trusting a decoded fallback cache."""
    try:
        uri = f"file:{os.path.abspath(path).replace(os.sep, '/')}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            return all(table in tables for table in TW_REQUIRED_TABLES)
    except (OSError, sqlite3.DatabaseError):
        return False


def _quick_check(path: str) -> bool:
    try:
        uri = f"file:{os.path.abspath(path).replace(os.sep, '/')}?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            return connection.execute('PRAGMA quick_check').fetchone() == ('ok',)
    except (OSError, sqlite3.DatabaseError):
        return False


def _valid_tw_database_file(path: str) -> bool:
    return (
        bool(path)
        and os.path.exists(path)
        and _valid_tw_cache(path)
        and _quick_check(path)
    )


def _first_valid_tw_database(paths) -> str:
    return next(
        (path for path in paths if _valid_tw_database_file(path)),
        None,
    )


def _valid_tw_cached_databases(region: str):
    return [
        path
        for path in _cached_databases(region)
        if _valid_tw_database_file(path)
    ]


def _is_tw_source_path(path: str, source: str) -> bool:
    if not path:
        return False
    source_dir = os.path.normcase(os.path.abspath(os.path.join(
        _db_dir(REGION_TW), source
    )))
    return os.path.normcase(os.path.dirname(os.path.abspath(path))) == source_dir


async def db_start(region: str = REGION_CN):
    if region == REGION_TW:
        return await ensure_database(region)

    os.makedirs(_db_dir(region), exist_ok=True)
    dbs = _cached_databases(region)
    if dbs:
        cached = max(dbs, key=_version_from_path)
        version = _version_from_path(cached)
    else:
        version = int(
            (await apiclient(
                bsdkclient(account('autopcr', 'autopcr', platform.Android))
            ).request(SourceIniGetMaintenanceStatusRequest())).manifest_ver
        )
    await datamgr.try_update_database(version, region)
    return version


async def _get_bytes(
    url: str,
    *,
    trust_env: bool = True,
    max_size: int = None,
) -> bytes:
    timeout = aiohttp.ClientTimeout(total=300)
    async with aiohttp.ClientSession(
        timeout=timeout,
        trust_env=trust_env,
    ) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            if (
                max_size is not None
                and response.content_length is not None
                and response.content_length > max_size
            ):
                raise ValueError(
                    f'Resource exceeds the {max_size}-byte download limit'
                )
            payload = bytearray()
            async for chunk in response.content.iter_chunked(256 * 1024):
                payload.extend(chunk)
                if max_size is not None and len(payload) > max_size:
                    raise ValueError(
                        f'Resource exceeds the {max_size}-byte download limit'
                    )
            return bytes(payload)


async def _get_json(url: str) -> dict:
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout, trust_env=True) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json(content_type=None)


async def _update_cn_database() -> int:
    """Preserve the existing CN database update path."""
    info = await _get_json(
        'https://redive.estertion.win/last_version_cn.json'
    )
    version_text = str(info['TruthVersion'])
    directory = _db_dir(REGION_CN)
    os.makedirs(directory, exist_ok=True)
    save_path = os.path.join(directory, f'{version_text}.db')
    if os.path.exists(save_path):
        return int(version_text)

    compressed = await _get_bytes(
        'https://redive.estertion.win/db/redive_cn.db.br'
    )
    decoded = brotli.decompress(compressed)
    if not decoded.startswith(b'SQLite format 3\x00'):
        raise ValueError('cn 数据库格式无效')

    temp_path = save_path + '.tmp'
    with open(temp_path, 'wb') as fp:
        fp.write(decoded)
    os.replace(temp_path, save_path)
    return int(version_text)


def _tw_region_info(info: dict) -> dict:
    regional = info.get('TW') or info.get('tw') or info
    if not isinstance(regional, dict):
        raise ValueError('台服数据库版本信息格式无效')
    return regional


def _tw_version(info: dict) -> int:
    regional = _tw_region_info(info)
    if 'version' not in regional:
        raise ValueError('无法从台服数据库版本信息中读取 TW.version')
    return int(str(regional['version']))


def _tw_mirror_hash(info: dict) -> str:
    return str(_tw_region_info(info).get('hash', '')).strip().lower()


def _tw_mirror_hash_path(database_path: str) -> str:
    return database_path + '.hash'


def _tw_mirror_cache_matches(path: str, expected_hash: str) -> bool:
    if not _valid_tw_database_file(path):
        return False
    if not expected_hash:
        return True
    try:
        with open(_tw_mirror_hash_path(path), 'r', encoding='ascii') as fp:
            return fp.read().strip().lower() == expected_hash
    except OSError:
        return False


def _first_matching_tw_mirror(paths, expected_hash: str) -> str:
    return next(
        (
            path for path in paths
            if _tw_mirror_cache_matches(path, expected_hash)
        ),
        None,
    )


def _write_tw_mirror_hash(database_path: str, value: str) -> None:
    path = _tw_mirror_hash_path(database_path)
    temp_path = f'{path}.{os.getpid()}.{uuid.uuid4().hex}.tmp'
    try:
        with open(temp_path, 'w', encoding='ascii') as fp:
            fp.write(value.strip().lower() + '\n')
        os.replace(temp_path, path)
    finally:
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass


def _prune_tw_mirror_variants(
    version: int,
    current_path: str,
    keep: int = 2,
) -> None:
    """Retain the active hash-qualified mirror and one rollback copy."""
    if keep < 1 or not _is_tw_source_path(current_path, 'mirror'):
        return
    directory = os.path.dirname(os.path.abspath(current_path))
    pattern = os.path.join(directory, f'{int(version):08d}-*.db')
    candidates = [
        os.path.abspath(path)
        for path in glob.glob(pattern)
        if os.path.isfile(path)
    ]
    current = os.path.abspath(current_path)
    if current not in candidates:
        return

    others = [path for path in candidates if path != current]
    others.sort(key=os.path.getmtime, reverse=True)
    retained = {current, *others[:keep - 1]}
    for path in candidates:
        if path in retained:
            continue
        for stale_path in (path, _tw_mirror_hash_path(path)):
            try:
                os.remove(stale_path)
            except FileNotFoundError:
                pass
            except OSError as ex:
                # Cleanup is best effort. A caller may still hold a session;
                # the next successful refresh can retry without blocking jobs.
                logger.warning(
                    'Unable to remove stale TW mirror cache %s: %s',
                    stale_path,
                    ex,
                )


def _build_tw_database(
    raw: bytes,
    save_path: str,
    version: int,
    decode_hashed_names: bool = True,
) -> None:
    """Atomically build a decoded TW database cache."""
    if not raw.startswith(b'SQLite format 3\x00'):
        raise ValueError('台服数据库格式无效')

    rainbow_path = os.getenv(
        'AUTOPCR_TW_RAINBOW_PATH',
        os.path.join(DATA_DIR, 'rainbow_tw.json'),
    )
    temp_path = f'{save_path}.{os.getpid()}.{uuid.uuid4().hex}.tmp'
    # Keep builders local: an executor task continues after its awaiting
    # coroutine is cancelled, and must not race another update through a
    # process-global SQLAlchemy engine.
    builder = dbmgr(f'{REGION_TW}-builder')
    try:
        with open(temp_path, 'wb') as fp:
            fp.write(raw)
        if decode_hashed_names:
            builder.load_db(temp_path, version)
            builder.unhash(
                rainbow_path,
                strict=True,
                required_tables=TW_REQUIRED_TABLES,
            )
            builder.dispose()
        if not _valid_tw_cache(temp_path) or not _quick_check(temp_path):
            raise ValueError('解码后的台服数据库完整性检查失败')
        os.replace(temp_path, save_path)
    finally:
        builder.dispose()
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _tw_official_version(resource_version: object = None) -> str:
    return normalize_tw_resource_version(
        resource_version
        or os.getenv('AUTOPCR_TW_RES_VERSION', '00500030')
    )


def _tw_bundle_cache_path(resource_version: str, xxhash64: str) -> str:
    return os.path.join(
        _db_dir(REGION_TW),
        'resources',
        f'{resource_version}-{xxhash64}.unity3d',
    )


def _read_valid_tw_resource(path: str, entry) -> bytes:
    try:
        if os.path.getsize(path) > TW_MAX_MASTER_BUNDLE_SIZE:
            raise ValueError('cached TW master bundle exceeds safety limit')
        with open(path, 'rb') as fp:
            payload = fp.read()
        validate_tw_resource(payload, entry)
        return payload
    except (OSError, ValueError):
        return b''


def _cache_tw_resource(path: str, payload: bytes) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = f'{path}.{os.getpid()}.{uuid.uuid4().hex}.tmp'
    try:
        with open(temp_path, 'wb') as fp:
            fp.write(payload)
        os.replace(temp_path, path)
    finally:
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            pass


async def _download_tw_official_master_bundle(
    resource_version: str,
):
    base_url = os.getenv(
        'AUTOPCR_TW_RESOURCE_BASE_URL',
        'https://img-pc.so-net.tw',
    ).strip().rstrip('/')
    trust_env = _env_flag('AUTOPCR_TW_USE_SYSTEM_PROXY', False)
    root_payload = await _get_bytes(
        tw_manifest_url(resource_version, TW_ROOT_MANIFEST, base_url),
        trust_env=trust_env,
        max_size=TW_MAX_MANIFEST_SIZE,
    )
    master_manifests = find_tw_master_manifests(
        parse_tw_manifest(root_payload)
    )
    if not master_manifests:
        raise ValueError('TW root manifest contains no master-data manifest')

    last_error = None
    master_entry = None
    for manifest_entry in master_manifests:
        if manifest_entry.size > TW_MAX_MANIFEST_SIZE:
            last_error = ValueError(
                f'TW manifest exceeds safety limit: {manifest_entry.name}'
            )
            continue
        try:
            manifest_payload = await _get_bytes(
                tw_manifest_url(
                    resource_version, manifest_entry.name, base_url
                ),
                trust_env=trust_env,
                max_size=manifest_entry.size,
            )
            validate_tw_resource(manifest_payload, manifest_entry)
            master_entry = find_tw_master_bundle(
                parse_tw_manifest(manifest_payload)
            )
            break
        except Exception as ex:
            last_error = ex
    if master_entry is None:
        raise ValueError(
            'Unable to resolve the TW master-data AssetBundle'
        ) from last_error
    if master_entry.size > TW_MAX_MASTER_BUNDLE_SIZE:
        raise ValueError('TW master-data AssetBundle exceeds safety limit')

    cache_path = _tw_bundle_cache_path(
        resource_version, master_entry.xxhash64
    )
    loop = asyncio.get_running_loop()
    bundle = await loop.run_in_executor(
        None, _read_valid_tw_resource, cache_path, master_entry
    )
    if not bundle:
        bundle = await _get_bytes(
            tw_bundle_url(master_entry.xxhash64, base_url),
            trust_env=trust_env,
            max_size=master_entry.size,
        )
        validate_tw_resource(bundle, master_entry)
        await asyncio.get_running_loop().run_in_executor(
            None, _cache_tw_resource, cache_path, bundle
        )
    # Extraction reopens the verified cache path.  Do not keep the bundle
    # bytes alive alongside UnityPy's decompressed objects and TextAsset.
    return cache_path, master_entry


async def _update_tw_official_database(
    resource_version: object = None,
) -> int:
    resource_version = _tw_official_version(resource_version)
    version = int(resource_version)
    save_path = _tw_database_path('official', version)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    loop = asyncio.get_running_loop()
    if await loop.run_in_executor(
        None, _valid_tw_database_file, save_path
    ):
        return version

    bundle_path, _ = await _download_tw_official_master_bundle(
        resource_version
    )
    raw = await loop.run_in_executor(
        None, extract_tw_master_database, bundle_path
    )
    await loop.run_in_executor(
        None, _build_tw_database, raw, save_path, version
    )
    return version


async def _update_tw_mirror_database():
    version_url = os.getenv(
        'AUTOPCR_TW_DB_VERSION_URL', TW_VERSION_URL
    ).strip()
    database_url = os.getenv(
        'AUTOPCR_TW_DB_URL', TW_DATABASE_URL
    ).strip()
    version_info = await _get_json(version_url)
    version = _tw_version(version_info)
    expected_hash = _tw_mirror_hash(version_info)
    # A mirror may republish corrected content without changing its numeric
    # version. Hash-qualified files avoid replacing an SQLite database that
    # is still open (which fails on Windows) and give dbmgr a new path so its
    # engine and generation-bound lazy caches are refreshed.
    save_path = _tw_database_path(
        'mirror', version, expected_hash or None
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cached_path = await asyncio.get_running_loop().run_in_executor(
        None,
        _first_matching_tw_mirror,
        (
            save_path,
            _tw_database_path('mirror', version),
            _legacy_tw_database_path(version),
        ),
        expected_hash,
    )
    if cached_path:
        return version, cached_path

    raw = await _get_bytes(
        database_url,
        max_size=TW_MAX_MIRROR_DATABASE_SIZE,
    )
    confirmed_info = await _get_json(version_url)
    confirmed_hash = _tw_mirror_hash(confirmed_info)
    if (
        _tw_version(confirmed_info) != version
        or confirmed_hash != expected_hash
    ):
        raise RuntimeError('台服数据库在下载过程中发生版本切换，请重试')
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, _build_tw_database, raw, save_path, version, False
    )
    if confirmed_hash:
        await loop.run_in_executor(
            None, _write_tw_mirror_hash, save_path, confirmed_hash
        )
    return version, save_path


async def _update_tw_database(
    resource_version: object = None,
    allow_mirror: bool = True,
):
    if _env_flag('AUTOPCR_TW_OFFICIAL_DB', True):
        try:
            version = await _update_tw_official_database(resource_version)
            return version, _tw_database_path('official', version)
        except Exception as ex:
            # Keep a decoded mirror/cache as a resilience path.  The official
            # resource failure remains visible so a changed bundle format or
            # manifest is diagnosable without breaking all TW daily jobs.
            if not allow_mirror:
                logger.warning(
                    'TW official master-data update failed; retaining the '
                    'current verified official cache: %s',
                    ex,
                )
                raise
            logger.warning(
                'TW official master-data update failed; using mirror fallback: %s',
                ex,
            )
    return await _update_tw_mirror_database()


async def do_update_database(
    region: str = REGION_CN,
    resource_version: object = None,
) -> int:
    if region == REGION_CN:
        return await _update_cn_database()
    if region == REGION_TW:
        version, _ = await _update_tw_database(resource_version)
        return version
    raise ValueError(f'Unsupported database region: {region}')


async def ensure_database(
    region: str = REGION_CN,
    resource_version: object = None,
) -> int:
    manager = get_dbmgr(region)
    if region == REGION_CN:
        if manager.ver is not None:
            db.get(region).update(manager)
            return manager.ver
        return await db_start(region)
    if region != REGION_TW:
        raise ValueError(f'Unsupported database region: {region}')

    requested_resource_version = _tw_official_version(resource_version)
    requested_cache = _tw_database_path(
        'official', int(requested_resource_version)
    )
    check_interval = max(
        60,
        int(os.getenv('AUTOPCR_TW_DB_CHECK_INTERVAL', '3600')),
    )
    # A mirror/legacy cache keeps jobs available, but should not suppress an
    # official retry for the whole normal refresh interval after a transient
    # CDN or extraction failure.
    active_check_interval = check_interval
    if (
        _env_flag('AUTOPCR_TW_OFFICIAL_DB', True)
        and manager._dbpath != requested_cache
    ):
        active_check_interval = min(check_interval, 300)
    if (
        manager.ver is not None
        and _database_resource_versions[region] == requested_resource_version
        and time.monotonic() - _database_checked_at[region]
        < active_check_interval
    ):
        db.get(region).update(manager)
        return manager.ver

    async with _database_locks[region]:
        if (
            manager.ver is not None
            and _database_resource_versions[region]
            == requested_resource_version
            and time.monotonic() - _database_checked_at[region]
            < active_check_interval
        ):
            db.get(region).update(manager)
            return manager.ver

        os.makedirs(_db_dir(region), exist_ok=True)
        loop = asyncio.get_running_loop()
        cached = await loop.run_in_executor(
            None, _valid_tw_cached_databases, region
        )
        try:
            keep_current_official = (
                _env_flag('AUTOPCR_TW_OFFICIAL_DB', True)
                and manager._dbpath in cached
                and _is_tw_source_path(manager._dbpath, 'official')
            )
            version, preferred_path = await _update_tw_database(
                requested_resource_version,
                allow_mirror=not keep_current_official,
            )
            candidates = [preferred_path]
            if version == int(requested_resource_version):
                candidates.append(_tw_database_path('official', version))
            candidates.extend((
                _tw_database_path('mirror', version),
                _legacy_tw_database_path(version),
            ))
            path = await loop.run_in_executor(
                None, _first_valid_tw_database, candidates
            )
            if path is None:
                raise ValueError('新下载的台服数据库缓存校验失败')
        except Exception as ex:
            # A transient GitHub/network outage must not stop daily tasks when
            # a previously decoded regional cache is available.
            logger.warning(
                '台服数据库更新失败，尝试使用已验证的本地缓存：%s', ex
            )
            if requested_cache in cached:
                path = requested_cache
                version = int(requested_resource_version)
            elif (
                manager.ver is not None
                and manager._dbpath in cached
            ):
                path = manager._dbpath
                version = manager.ver
            elif cached:
                path = max(cached, key=os.path.getmtime)
                version = _version_from_path(path)
            else:
                raise

        if manager.ver != version or manager._dbpath != path:
            manager.load_db(path, version)
        if _is_tw_source_path(path, 'mirror'):
            await loop.run_in_executor(
                None, _prune_tw_mirror_variants, version, path
            )
        db.get(region).update(manager)
        _database_checked_at[region] = time.monotonic()
        _database_resource_versions[region] = requested_resource_version
        return version
