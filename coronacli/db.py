from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date, Numeric

SQLITE = 'sqlite'
# TODO make date strings actual Date types
TABLES = {
    'owid_covid_data': {
        'table_name': 'owid_covid_data',
        'schema': [
        {'col_name': 'country_code', 'col_obj': Column('country_code', String)},
        {'col_name': 'date', 'col_obj': Column('date', String)},
        {'col_name': 'total_cases', 'col_obj': Column('total_cases', Integer)},
        {'col_name': 'new_cases', 'col_obj': Column('new_cases', Integer)},
        {'col_name': 'total_deaths', 'col_obj': Column('total_deaths', Integer)},
        {'col_name': 'new_deaths', 'col_obj': Column('total_deaths', Integer)},
        {'col_name': 'total_cases_per_million', 'col_obj': Column('total_cases_per_million', Numeric(38, 7))},
        {'col_name': 'new_cases_per_million', 'col_obj': Column('new_cases_per_million', Numeric(38, 7))},
        {'col_name': 'total_deaths_per_million', 'col_obj': Column('total_deaths_per_million', Numeric(38, 7))},
        {'col_name': 'new_deaths_per_million', 'col_obj': Column('new_deaths_per_million', Numeric(38, 7))}
        ]
    },
    'owid_country_data': {
        'table_name': 'owid_country_data',
        'schema': [
        {'col_name': 'country_code', 'col_obj': Column('country_code', String)},
        {'col_name': 'location', 'col_obj': Column('location', String)},
        {'col_name': 'continent', 'col_obj': Column('continent', String)},
        {'col_name': 'population', 'col_obj': Column('population', Integer)},
        {'col_name': 'population_density', 'col_obj': Column('population_density', Numeric(38, 7))},
        {'col_name': 'aged_65_older', 'col_obj': Column('aged_65_older', Numeric(38, 7))},
        {'col_name': 'aged_70_older', 'col_obj': Column('aged_70_older', Numeric(38, 7))},
        {'col_name': 'gdp_per_capita', 'col_obj': Column('gdp_per_capita', Numeric(38, 7))},
        {'col_name': 'cardiovasc_death_rate', 'col_obj': Column('cardiovasc_death_rate', Numeric(38, 7))},
        {'col_name': 'diabetes_prevalence', 'col_obj': Column('diabetes_prevalence', Numeric(38, 7))},
        {'col_name': 'handwashing_facilities', 'col_obj': Column('handwashing_facilities', Numeric(38, 7))},
        {'col_name': 'hospital_beds_per_thousand', 'col_obj': Column('hospital_beds_per_thousand', Numeric(38, 7))},
        {'col_name': 'life_expectancy', 'col_obj': Column('life_expectancy', Numeric(38, 7))}
        ]
    }
}


class DB:

    DB_ENGINE = {SQLITE: 'sqlite:///{DB}'}

    def __init__(self, dbname, dbtype=SQLITE):
        self.dbtype = dbtype.lower()
        self.dbname = dbname
        self.owid_table = None

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

    def execute_query(self, query):
        with self.db_engine.connect() as connection:
            connection.execute(query)

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

    def insert_into_table(self, table_name, values):
        """ Inserts the given values into the given table in the database

        :param table_name - the name of the table to insert record values into
        :param values - a list of lists of values to insert into, one sublist per record
        """
        col_names = ', '.join(self.get_column_names_from_schema(table_name))
        # TODO wrap date and timestamp values in single quotes; move to utils.py
        # TODO Construct query first with all records then execute once instead of for each record
        for value_obj in values:
            record = ', '.join(
                ["'{0}'".format(val) if isinstance(val, str) else str(val) for val in value_obj])
            query = "INSERT INTO {0}({1}) VALUES({2});".format(table_name, col_names, record)
            self.execute_query(query)
