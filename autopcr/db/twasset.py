"""Taiwan official resource-manifest and master-data helpers.

The TW client does not publish a raw SQLite database.  It resolves the
``a/masterdata_master.unity3d`` entry through the resource manifests, downloads
the content-addressed AssetBundle, and extracts the ``master`` TextAsset.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import md5
import os
import re
import threading
from typing import Iterable, Union

import UnityPy
from UnityPy.enums import ClassIDType
from UnityPy.helpers import ArchiveStorageManager


TW_RESOURCE_BASE_URL = "https://img-pc.so-net.tw"
TW_MASTER_ASSET = "a/masterdata_master.unity3d"
TW_ROOT_MANIFEST = "manifest/manifest_assetmanifest"

_MD5_RE = re.compile(r"[0-9a-fA-F]{32}")
_XXHASH64_RE = re.compile(r"[0-9a-fA-F]{16}")
# UnityPy stores its fallback version and China-bundle key in process globals.
# CN's asset manager shares this lock so a TW update cannot change that state
# midway through another region's bundle read.
UNITYPY_LOCK = threading.Lock()


@dataclass(frozen=True)
class TwManifestEntry:
    name: str
    md5: str
    xxhash64: str
    category: str
    size: int

    @classmethod
    def from_line(cls, line: str) -> "TwManifestEntry":
        fields = line.rstrip("\r").split(",")
        if len(fields) < 5:
            raise ValueError(f"Invalid TW manifest row: {line!r}")
        name, md5_text, xxhash64, category, size_text = fields[:5]
        if not name or not _MD5_RE.fullmatch(md5_text):
            raise ValueError(f"Invalid TW manifest name or MD5: {line!r}")
        if not _XXHASH64_RE.fullmatch(xxhash64):
            raise ValueError(f"Invalid TW manifest XXHash64: {line!r}")
        try:
            size = int(size_text)
        except ValueError as ex:
            raise ValueError(f"Invalid TW manifest size: {line!r}") from ex
        if size < 0:
            raise ValueError(f"Invalid TW manifest size: {line!r}")
        return cls(
            name=name,
            md5=md5_text.lower(),
            xxhash64=xxhash64.lower(),
            category=category,
            size=size,
        )


def parse_tw_manifest(payload: bytes | str) -> list[TwManifestEntry]:
    if isinstance(payload, bytes):
        text = payload.decode("utf-8-sig")
    else:
        text = payload
    return [
        TwManifestEntry.from_line(line)
        for line in text.splitlines()
        if line.strip()
    ]


def normalize_tw_resource_version(value: object) -> str:
    version = str(value or "").strip()
    if not version.isdigit() or len(version) > 12:
        raise ValueError(f"Invalid TW resource version: {value!r}")
    return version.zfill(8)


def tw_manifest_url(
    resource_version: object,
    name: str,
    base_url: str = TW_RESOURCE_BASE_URL,
) -> str:
    version = normalize_tw_resource_version(resource_version)
    if not name.startswith("manifest/") or ".." in name.split("/"):
        raise ValueError(f"Invalid TW manifest path: {name!r}")
    return (
        f"{base_url.rstrip('/')}/dl/Resources/{version}/Jpn/"
        f"AssetBundles/Android/{name}"
    )


def tw_bundle_url(
    xxhash64: str,
    base_url: str = TW_RESOURCE_BASE_URL,
) -> str:
    value = xxhash64.lower()
    if not _XXHASH64_RE.fullmatch(value):
        raise ValueError(f"Invalid TW bundle XXHash64: {xxhash64!r}")
    return (
        f"{base_url.rstrip('/')}/dl/pool/AssetBundles/"
        f"{value[:2]}/{value}"
    )


def validate_tw_resource(payload: bytes, entry: TwManifestEntry) -> None:
    if len(payload) != entry.size:
        raise ValueError(
            f"TW resource size mismatch for {entry.name}: "
            f"expected {entry.size}, got {len(payload)}"
        )
    digest = md5(payload).hexdigest()
    if digest != entry.md5:
        raise ValueError(
            f"TW resource MD5 mismatch for {entry.name}: "
            f"expected {entry.md5}, got {digest}"
        )


def find_tw_master_manifests(
    entries: Iterable[TwManifestEntry],
) -> list[TwManifestEntry]:
    candidates = [
        entry
        for entry in entries
        if entry.name.startswith("manifest/masterdata")
        and entry.name.endswith("_assetmanifest")
    ]
    # New clients may publish masterdata2 alongside the legacy manifest.
    def generation(entry: TwManifestEntry) -> tuple[int, str]:
        match = re.search(r"/masterdata(\d*)_assetmanifest$", entry.name)
        return (int(match.group(1) or 0) if match else -1, entry.name)

    return sorted(candidates, key=generation, reverse=True)


def find_tw_master_bundle(
    entries: Iterable[TwManifestEntry],
) -> TwManifestEntry:
    try:
        return next(entry for entry in entries if entry.name == TW_MASTER_ASSET)
    except StopIteration as ex:
        raise ValueError(
            f"{TW_MASTER_ASSET} is absent from the TW master manifest"
        ) from ex


def _assetbundle_key(value: str | bytes | None) -> bytes | None:
    if value is None:
        value = os.getenv("AUTOPCR_TW_ASSETBUNDLE_KEY", "")
    if value in (b"", ""):
        return None
    if isinstance(value, bytes):
        key = value
    elif value.startswith("hex:"):
        try:
            key = bytes.fromhex(value[4:])
        except ValueError as ex:
            raise ValueError("Invalid hex TW AssetBundle key") from ex
    else:
        key = value.encode("utf-8", "surrogateescape")
    if len(key) != 16:
        raise ValueError(
            "AUTOPCR_TW_ASSETBUNDLE_KEY must contain exactly 16 bytes"
        )
    return key


def extract_tw_master_database(
    bundle: Union[bytes, str, os.PathLike],
    *,
    key: str | bytes | None = None,
    unity_version: str | None = None,
) -> bytes:
    """Extract the raw SQLite TextAsset from a verified TW AssetBundle.

    UnityPy keeps its fallback Unity version and China-bundle key in module
    globals.  Serialize and restore that state so CN asset reads remain
    unaffected even when regional accounts run concurrently.
    """

    parsed_version = tuple(
        int(part)
        for part in re.findall(
            r"\d+", str(getattr(UnityPy, "__version__", "0"))
        )[:3]
    )
    version_parts = (parsed_version + (0, 0, 0))[:3]
    if version_parts < (1, 25, 0):
        raise RuntimeError(
            "UnityPy >= 1.25.0 is required for TW Unity 6000 bundles"
        )

    decrypt_key = _assetbundle_key(key)
    fallback_version = unity_version or os.getenv(
        "AUTOPCR_TW_UNITY_VERSION", "6000.0.58f2"
    )
    # UnityPy accepts a filesystem path as str, but not pathlib.Path on
    # Windows even though both satisfy os.PathLike.
    source = os.fspath(bundle) if isinstance(bundle, os.PathLike) else bundle
    with UNITYPY_LOCK:
        previous_version = UnityPy.config.FALLBACK_UNITY_VERSION
        previous_key = ArchiveStorageManager.DECRYPT_KEY
        try:
            UnityPy.config.FALLBACK_UNITY_VERSION = fallback_version
            if decrypt_key is not None:
                UnityPy.set_assetbundle_decrypt_key(decrypt_key)
            environment = UnityPy.load(source)
            for obj in environment.objects:
                if obj.type != ClassIDType.TextAsset:
                    continue
                asset = obj.read()
                name = getattr(asset, "m_Name", getattr(asset, "name", None))
                if name == "master":
                    script = getattr(
                        asset,
                        "m_Script",
                        getattr(asset, "script", None),
                    )
                    if isinstance(script, str):
                        # UnityPy 1.25 exposes TextAsset.m_Script as text and
                        # decodes arbitrary bytes with surrogateescape.
                        database = script.encode("utf-8", "surrogateescape")
                    elif script is not None:
                        database = bytes(script)
                    else:
                        raise ValueError(
                            "TW master TextAsset contains no script payload"
                        )
                    if not database.startswith(b"SQLite format 3\x00"):
                        raise ValueError(
                            "TW master TextAsset is not an SQLite database"
                        )
                    return database
        finally:
            UnityPy.config.FALLBACK_UNITY_VERSION = previous_version
            ArchiveStorageManager.DECRYPT_KEY = previous_key
    raise ValueError("TW master AssetBundle contains no 'master' TextAsset")
