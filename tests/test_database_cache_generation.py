import os
import sqlite3
import tempfile
import unittest

from sqlalchemy import text

# Bootstrap the existing core package import order before importing database
# directly; database.py itself references core.apiclient.
from autopcr.core.apiclient import apiclient  # noqa: F401
from autopcr.db.database import database, lazy_property
from autopcr.db.dbmgr import dbmgr


class _ProbeDatabase(database):
    @lazy_property
    def marker(self):
        with self.dbmgr.session() as session:
            return session.execute(text("SELECT value FROM marker")).scalar_one()


class DatabaseCacheGenerationTests(unittest.TestCase):
    @staticmethod
    def _create(path, value):
        connection = sqlite3.connect(path)
        try:
            connection.execute("CREATE TABLE marker (value TEXT NOT NULL)")
            connection.execute("INSERT INTO marker VALUES (?)", (value,))
            connection.commit()
        finally:
            connection.close()

    def test_same_numeric_version_reloads_lazy_values_after_source_switch(self):
        manager = dbmgr("cache-generation-test")
        regional = _ProbeDatabase()
        with tempfile.TemporaryDirectory() as directory:
            official = os.path.join(directory, "official.db")
            mirror = os.path.join(directory, "mirror.db")
            self._create(official, "official")
            self._create(mirror, "mirror")
            try:
                manager.load_db(official, 600001)
                regional.update(manager)
                self.assertEqual("official", regional.marker)

                manager.load_db(mirror, 600001)
                regional.update(manager)
                self.assertEqual("mirror", regional.marker)
            finally:
                manager.dispose()


if __name__ == "__main__":
    unittest.main()
