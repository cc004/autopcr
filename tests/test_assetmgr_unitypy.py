import unittest
from types import SimpleNamespace
from unittest.mock import patch

from autopcr.db.assetmgr import _load_database


class AssetManagerUnityPyCompatibilityTests(unittest.TestCase):
    def _load(self, **asset_fields):
        environment = SimpleNamespace(
            objects=[SimpleNamespace(
                read=lambda: SimpleNamespace(**asset_fields)
            )]
        )
        with patch(
            "autopcr.db.assetmgr.UnityPy.load",
            return_value=environment,
        ):
            return _load_database(b"bundle")

    def test_loads_legacy_bytes_script(self):
        self.assertEqual(b"database", self._load(script=b"database"))

    def test_loads_unitypy_125_text_script_losslessly(self):
        raw = b"SQLite format 3\x00\xffdatabase"
        text = raw.decode("utf-8", "surrogateescape")
        self.assertEqual(raw, self._load(m_Script=text))


if __name__ == "__main__":
    unittest.main()
