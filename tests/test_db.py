import pytest

from sqlalchemy import exc

from coronacli import db
from coronacli.config import SQLITE, TABLES


DB_NAME = "test_db"
DB_TYPES = [SQLITE]
DB_LIST = [db.DB("{0}_{1}".format(DB_NAME, db_type), db_type) for db_type in DB_TYPES]


def test_create_tables():
    table_collection = TABLES
    for test_db in DB_LIST:
        # Create tables from config collection of tables
        test_db.create_tables(table_collection)
        # Check that tables created exist
        for table, _ in table_collection.items():
            test_db.execute_query("SELECT * FROM {0}".format(table))


def test_drop_tables():
    table_collection = TABLES
    for test_db in DB_LIST:
        # Drop all tables in db
        test_db.drop_tables(table_collection)
        for table, _ in table_collection.items():
            # Check that tables no longer exist
            with pytest.raises(exc.OperationalError):
                test_db.execute_query("SELECT * FROM {0}".format(table))


def test_db_drop():
    for test_db in DB_LIST:
        test_db.drop()
        assert not db.DB.db_exists(test_db.dbname, test_db.dbtype)
