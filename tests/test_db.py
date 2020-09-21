import pytest

from sqlalchemy import exc

from coronacli import db
from coronacli.config import TABLES
from tests import resources


def test_drop_tables():
    table_collection = TABLES
    for test_db in resources.DB_LIST:
        # Drop all tables in db
        test_db.drop_tables(table_collection)
        for table, _ in table_collection.items():
            # Check that tables no longer exist
            with pytest.raises(exc.OperationalError):
                test_db.execute_query("SELECT * FROM {0}".format(table))


def test_db_drop():
    for test_db in resources.DB_LIST:
        test_db.drop()
        assert not db.DB.db_exists(test_db.dbname, test_db.dbtype)
