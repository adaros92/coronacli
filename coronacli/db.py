from sqlalchemy import create_engine, Table, MetaData

from coronacli.config import TABLES, SQLITE


class DB:

    DB_ENGINE = {SQLITE: 'sqlite:///{DB}'}

    def __init__(self, dbname, dbtype=SQLITE):
        self.dbtype = dbtype.lower()
        self.dbname = dbname

        engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
        self.db_engine = create_engine(engine_url)

    def create_tables(self, table_collection=None):
        metadata = MetaData()
        if not table_collection:
            table_collection = TABLES
        for table, table_map in table_collection.items():
            table_name = table_map['table_name']
            columns = self.get_column_objects_from_schema(table_name)
            Table(table_name, metadata, *columns)
        metadata.create_all(self.db_engine)

    def execute_query(self, query, expect_results=False):
        connection = self.db_engine.connect()
        execution = connection.execute(query)
        results = None
        if expect_results:
            results = execution.fetchall()
        connection.close()
        return results

    @staticmethod
    def get_cols_from_schema(table_name, table_collection=None):
        cols = []
        if not table_collection:
            table_collection = TABLES
        for col in table_collection[table_name]['schema']:
            cols.append(col)
        return cols

    @staticmethod
    def get_column_names_from_schema(table_name, table_collection=None):
        cols = DB.get_cols_from_schema(table_name, table_collection)
        return [col['col_name'] for col in cols]

    @staticmethod
    def get_column_objects_from_schema(table_name, table_collection=None):
        cols = DB.get_cols_from_schema(table_name, table_collection)
        return [col['col_obj'] for col in cols]

    def insert_into_table(self, table_name, col_names, values):
        """ Inserts the given values into the given table in the database

        :param table_name - the name of the table to insert record values into
        :param col_names - a list of column names in same order as given values
        :param values - a list of lists of values to insert into, one sublist per record
        """
        # TODO wrap date and timestamp values in single quotes; move to utils.py
        # TODO Construct query first with all records then execute once instead of for each record
        assert len(col_names) == len(values)
        for idx, value_obj in enumerate(values):
            record = ', '.join(
                ["'{0}'".format(val) if isinstance(val, str) else str(val) for val in value_obj])
            cols = ', '.join(col_names[idx])
            query = "INSERT INTO {0}({1}) VALUES({2});".format(table_name, cols, record)
            self.execute_query(query)

    def select_all_from_table(self, table_name):
        query = "SELECT * FROM {0};".format(table_name)
        return self.execute_query(query, expect_results=True)
