import asyncio
import hashlib
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from sqlalchemy import text
from UnityPy.enums import ClassIDType
from UnityPy.helpers import ArchiveStorageManager

from autopcr.db import dbstart
from autopcr.db.dbmgr import dbmgr
from autopcr.db.twasset import (
    TW_MASTER_ASSET,
    TW_ROOT_MANIFEST,
    TwManifestEntry,
    extract_tw_master_database,
    find_tw_master_bundle,
    find_tw_master_manifests,
    normalize_tw_resource_version,
    parse_tw_manifest,
    tw_bundle_url,
    tw_manifest_url,
    validate_tw_resource,
)


def _entry(name: str, payload: bytes, xxhash64: str) -> TwManifestEntry:
    return TwManifestEntry(
        name=name,
        md5=hashlib.md5(payload).hexdigest(),
        xxhash64=xxhash64,
        category="every",
        size=len(payload),
    )


def _line(entry: TwManifestEntry) -> bytes:
    return (
        f"{entry.name},{entry.md5},{entry.xxhash64},"
        f"{entry.category},{entry.size},\n"
    ).encode()


class TaiwanManifestTests(unittest.TestCase):
    def test_parse_current_five_field_manifest_and_urls(self):
        row = (
            "a/masterdata_master.unity3d,"
            "8f3d0117a78a2f379c05366154bd9c53,"
            "4268ccc78bb697c8,tutorial0,13847670,\n"
        )
        entry = parse_tw_manifest(row)[0]

        self.assertEqual(TW_MASTER_ASSET, entry.name)
        self.assertEqual("4268ccc78bb697c8", entry.xxhash64)
        self.assertEqual(13847670, entry.size)
        self.assertEqual("00500029", normalize_tw_resource_version(500029))
        self.assertEqual(
            "https://img-pc.so-net.tw/dl/Resources/00500029/Jpn/"
            "AssetBundles/Android/manifest/manifest_assetmanifest",
            tw_manifest_url("00500029", TW_ROOT_MANIFEST),
        )
        self.assertEqual(
            "https://img-pc.so-net.tw/dl/pool/AssetBundles/42/"
            "4268ccc78bb697c8",
            tw_bundle_url(entry.xxhash64),
        )

    def test_manifest_selection_and_integrity_validation(self):
        payload = b"master manifest"
        master_manifest = _entry(
            "manifest/masterdata2_assetmanifest",
            payload,
            "740b11e9f98ad15d",
        )
        legacy_manifest = _entry(
            "manifest/masterdata_assetmanifest",
            payload,
            "640b11e9f98ad15d",
        )
        bundle = _entry(TW_MASTER_ASSET, b"bundle", "4268ccc78bb697c8")

        self.assertEqual(
            [master_manifest, legacy_manifest],
            find_tw_master_manifests([legacy_manifest, master_manifest]),
        )
        self.assertEqual(bundle, find_tw_master_bundle([bundle]))
        validate_tw_resource(payload, master_manifest)
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            validate_tw_resource(payload + b"!", master_manifest)


class TaiwanOfficialDownloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_resolves_manifests_validates_and_caches_bundle(self):
        bundle_payload = b"encrypted master bundle"
        bundle_entry = _entry(
            TW_MASTER_ASSET, bundle_payload, "4268ccc78bb697c8"
        )
        child_payload = _line(bundle_entry)
        child_entry = _entry(
            "manifest/masterdata2_assetmanifest",
            child_payload,
            "740b11e9f98ad15d",
        )
        root_payload = _line(child_entry)
        expected_urls = {
            tw_manifest_url("00500029", TW_ROOT_MANIFEST): root_payload,
            tw_manifest_url("00500029", child_entry.name): child_payload,
            tw_bundle_url(bundle_entry.xxhash64): bundle_payload,
        }

        async def get_bytes(url, **_kwargs):
            return expected_urls[url]

        with tempfile.TemporaryDirectory() as directory, patch.object(
            dbstart, "CACHE_DIR", directory
        ), patch.object(dbstart, "_get_bytes", side_effect=get_bytes) as fetch:
            bundle_path, selected = (
                await dbstart._download_tw_official_master_bundle("00500029")
            )
            bundle_path_again, _ = (
                await dbstart._download_tw_official_master_bundle("00500029")
            )
            downloaded = Path(bundle_path).read_bytes()

        self.assertEqual(bundle_payload, downloaded)
        self.assertEqual(bundle_path, bundle_path_again)
        self.assertEqual(bundle_entry, selected)
        # Manifests are refreshed, while the verified bundle is reused.
        self.assertEqual(5, fetch.call_count)

    async def test_official_failure_uses_existing_mirror_path(self):
        with patch.object(
            dbstart,
            "_update_tw_official_database",
            new=AsyncMock(side_effect=ValueError("changed bundle format")),
        ) as official, patch.object(
            dbstart,
            "_update_tw_mirror_database",
            new=AsyncMock(return_value=(600001, "mirror.db")),
        ) as mirror:
            version, path = await dbstart._update_tw_database("00500029")

        self.assertEqual(600001, version)
        self.assertEqual("mirror.db", path)
        official.assert_awaited_once_with("00500029")
        mirror.assert_awaited_once_with()

    async def test_cn_update_path_is_unchanged(self):
        with patch.object(
            dbstart,
            "_update_cn_database",
            new=AsyncMock(return_value=123456),
        ) as update_cn, patch.object(
            dbstart,
            "_update_tw_database",
            new=AsyncMock(),
        ) as update_tw:
            version = await dbstart.do_update_database("cn", "00500029")

        self.assertEqual(123456, version)
        update_cn.assert_awaited_once_with()
        update_tw.assert_not_awaited()

    async def test_tw_public_update_returns_numeric_version(self):
        update = AsyncMock(return_value=(600001, "mirror.db"))
        with patch.object(dbstart, "_update_tw_database", new=update):
            version = await dbstart.do_update_database(
                "tw", "00500030"
            )

        self.assertEqual(600001, version)
        update.assert_awaited_once_with("00500030")


class TaiwanDatabaseBuildTests(unittest.TestCase):
    @staticmethod
    def _decoded_database() -> bytes:
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "decoded.db")
            connection = sqlite3.connect(path)
            try:
                for table in dbstart.TW_REQUIRED_TABLES:
                    connection.execute(
                        f'CREATE TABLE "{table}" (id INTEGER PRIMARY KEY)'
                    )
                connection.commit()
            finally:
                connection.close()
            with open(path, "rb") as fp:
                return fp.read()

    def test_builds_already_decoded_mirror_without_rainbow_rewrite(self):
        raw = self._decoded_database()
        with tempfile.TemporaryDirectory() as directory:
            save_path = os.path.join(directory, "mirror", "00600001.db")
            os.makedirs(os.path.dirname(save_path))

            dbstart._build_tw_database(
                raw,
                save_path,
                600001,
                decode_hashed_names=False,
            )

            self.assertTrue(dbstart._valid_tw_cache(save_path))
            self.assertTrue(dbstart._quick_check(save_path))

    def test_official_and_mirror_cache_namespaces_do_not_collide(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            dbstart, "CACHE_DIR", directory
        ):
            official = dbstart._tw_database_path("official", 500029)
            mirror = dbstart._tw_database_path("mirror", 500029)

        self.assertNotEqual(official, mirror)
        self.assertIn(os.path.join("tw", "official"), official)
        self.assertIn(os.path.join("tw", "mirror"), mirror)

    def test_mirror_cache_is_bound_to_upstream_hash(self):
        raw = self._decoded_database()
        with tempfile.TemporaryDirectory() as directory:
            save_path = os.path.join(directory, "mirror", "00600001.db")
            os.makedirs(os.path.dirname(save_path))
            dbstart._build_tw_database(
                raw, save_path, 600001, decode_hashed_names=False
            )

            self.assertFalse(
                dbstart._tw_mirror_cache_matches(save_path, "old-hash")
            )
            dbstart._write_tw_mirror_hash(save_path, "old-hash")
            self.assertTrue(
                dbstart._tw_mirror_cache_matches(save_path, "old-hash")
            )
            self.assertFalse(
                dbstart._tw_mirror_cache_matches(save_path, "new-hash")
            )

    def test_flat_mirror_version_json_exposes_hash(self):
        info = {"version": "600001", "hash": "ABCDEF0123456789"}
        self.assertEqual(600001, dbstart._tw_version(info))
        self.assertEqual("abcdef0123456789", dbstart._tw_mirror_hash(info))

    def test_hash_qualified_mirror_paths_keep_numeric_version(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(
            dbstart, "CACHE_DIR", directory
        ):
            first = dbstart._tw_database_path(
                "mirror", 600001, "a" * 16
            )
            second = dbstart._tw_database_path(
                "mirror", 600001, "b" * 16
            )

        self.assertNotEqual(first, second)
        self.assertEqual(600001, dbstart._version_from_path(first))


class TaiwanDatabaseFallbackTests(unittest.IsolatedAsyncioTestCase):
    async def test_same_version_new_mirror_hash_switches_open_database(self):
        raw = TaiwanDatabaseBuildTests._decoded_database()
        manager = dbmgr("tw-hash-refresh-test")
        regional = SimpleNamespace(update=Mock())
        router = SimpleNamespace(get=lambda _region: regional)
        previous_lock = dbstart._database_locks["tw"]
        previous_resource = dbstart._database_resource_versions["tw"]
        previous_checked = dbstart._database_checked_at["tw"]
        old_hash = "a" * 16
        new_hash = "b" * 16
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(
                dbstart, "CACHE_DIR", directory
            ):
                stale_path = dbstart._tw_database_path(
                    "mirror", 600001, "c" * 16
                )
                old_path = dbstart._tw_database_path(
                    "mirror", 600001, old_hash
                )
                os.makedirs(os.path.dirname(old_path), exist_ok=True)
                dbstart._build_tw_database(
                    raw, stale_path, 600001, decode_hashed_names=False
                )
                dbstart._write_tw_mirror_hash(stale_path, "c" * 16)
                os.utime(stale_path, (1, 1))
                dbstart._build_tw_database(
                    raw, old_path, 600001, decode_hashed_names=False
                )
                dbstart._write_tw_mirror_hash(old_path, old_hash)
                manager.load_db(old_path, 600001)
                # Return a connection to SQLAlchemy's pool so the old file is
                # genuinely still open on Windows during the refresh.
                with manager.session() as session:
                    session.execute(text("SELECT 1")).scalar()

                info = {"version": "600001", "hash": new_hash}
                with patch.object(
                    dbstart,
                    "_get_json",
                    new=AsyncMock(side_effect=[info, info]),
                ), patch.object(
                    dbstart, "_get_bytes", new=AsyncMock(return_value=raw)
                ):
                    version, new_path = (
                        await dbstart._update_tw_mirror_database()
                    )

                self.assertEqual(600001, version)
                self.assertNotEqual(old_path, new_path)
                self.assertTrue(os.path.exists(old_path))
                self.assertTrue(os.path.exists(new_path))

                initial_generation = manager.generation
                dbstart._database_locks["tw"] = asyncio.Lock()
                dbstart._database_resource_versions["tw"] = None
                dbstart._database_checked_at["tw"] = 0.0
                update = AsyncMock(return_value=(version, new_path))
                with patch.object(
                    dbstart, "get_dbmgr", return_value=manager
                ), patch.object(dbstart, "db", router), patch.object(
                    dbstart, "_update_tw_database", new=update
                ):
                    loaded_version = await dbstart.ensure_database(
                        "tw", "00500030"
                    )

                self.assertEqual(version, loaded_version)
                self.assertEqual(new_path, manager._dbpath)
                self.assertEqual(
                    initial_generation + 1, manager.generation
                )
                self.assertFalse(os.path.exists(stale_path))
                self.assertFalse(
                    os.path.exists(dbstart._tw_mirror_hash_path(stale_path))
                )

                # Once load_db has disposed the old engine, Windows also
                # permits deleting the formerly active file.
                dbstart._prune_tw_mirror_variants(
                    version, new_path, keep=1
                )
                self.assertFalse(os.path.exists(old_path))
        finally:
            manager.dispose()
            dbstart._database_locks["tw"] = previous_lock
            dbstart._database_resource_versions["tw"] = previous_resource
            dbstart._database_checked_at["tw"] = previous_checked

    async def test_new_official_failure_keeps_loaded_verified_official(self):
        raw = TaiwanDatabaseBuildTests._decoded_database()
        manager = dbmgr("tw-fallback-test")
        regional = SimpleNamespace(update=Mock())
        router = SimpleNamespace(get=lambda _region: regional)
        previous_lock = dbstart._database_locks["tw"]
        previous_resource = dbstart._database_resource_versions["tw"]
        previous_checked = dbstart._database_checked_at["tw"]
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(
                dbstart, "CACHE_DIR", directory
            ):
                official = dbstart._tw_database_path("official", 500030)
                os.makedirs(os.path.dirname(official), exist_ok=True)
                dbstart._build_tw_database(
                    raw, official, 500030, decode_hashed_names=False
                )
                manager.load_db(official, 500030)
                dbstart._database_locks["tw"] = asyncio.Lock()
                dbstart._database_resource_versions["tw"] = None
                dbstart._database_checked_at["tw"] = 0.0

                update = AsyncMock(side_effect=ValueError("temporary CDN"))
                with patch.object(
                    dbstart, "get_dbmgr", return_value=manager
                ), patch.object(dbstart, "db", router), patch.object(
                    dbstart, "_update_tw_database", new=update
                ):
                    version = await dbstart.ensure_database(
                        "tw", "00500031"
                    )

                self.assertEqual(500030, version)
                self.assertEqual(official, manager._dbpath)
                update.assert_awaited_once_with(
                    "00500031", allow_mirror=False
                )
        finally:
            manager.dispose()
            dbstart._database_locks["tw"] = previous_lock
            dbstart._database_resource_versions["tw"] = previous_resource
            dbstart._database_checked_at["tw"] = previous_checked


class TaiwanBundleExtractionTests(unittest.TestCase):
    def _extract(self, script):
        sqlite = b"SQLite format 3\x00" + b"database"
        asset = SimpleNamespace(m_Name="master", **script(sqlite))
        obj = SimpleNamespace(
            type=ClassIDType.TextAsset,
            read=lambda: asset,
        )
        environment = SimpleNamespace(objects=[obj])
        old_key = ArchiveStorageManager.DECRYPT_KEY

        with patch(
            "autopcr.db.twasset.UnityPy.__version__", "1.25.0"
        ), patch(
            "autopcr.db.twasset.UnityPy.load", return_value=environment
        ):
            result = extract_tw_master_database(
                b"bundle", key=b"0123456789abcdef"
            )

        self.assertEqual(sqlite, result)
        self.assertIs(ArchiveStorageManager.DECRYPT_KEY, old_key)

    def test_extracts_legacy_bytes_script_and_restores_unitypy_globals(self):
        self._extract(lambda sqlite: {"script": sqlite})

    def test_extracts_unitypy_125_text_script_losslessly(self):
        self._extract(
            lambda sqlite: {
                "m_Script": sqlite.decode("utf-8", "surrogateescape")
            }
        )

    def test_rejects_unitypy_that_misclassifies_unity_6000_bundle(self):
        with patch(
            "autopcr.db.twasset.UnityPy.__version__", "1.10.18"
        ), self.assertRaisesRegex(RuntimeError, "UnityPy >= 1.25.0"):
            extract_tw_master_database(b"bundle")

    def test_pathlike_bundle_is_forwarded_as_native_path_string(self):
        bundle = Path("masterdata_master.unity3d")
        environment = SimpleNamespace(objects=[])
        with patch(
            "autopcr.db.twasset.UnityPy.__version__", "1.25.0"
        ), patch(
            "autopcr.db.twasset.UnityPy.load", return_value=environment
        ) as load, self.assertRaisesRegex(ValueError, "TextAsset"):
            extract_tw_master_database(bundle)

        load.assert_called_once_with(os.fspath(bundle))


if __name__ == "__main__":
    unittest.main()
