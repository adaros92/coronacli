from coronacli import config, db


DB_NAME = "test_db"
DB_TYPES = [config.SQLITE]
DB_LIST = [db.DB("{0}_{1}".format(DB_NAME, db_type), db_type) for db_type in DB_TYPES]
OWID_CASES_SAMPLE_DATA = [
    ['USA', '2020-08-01', 13232, 2324, 4321, 32334, 767, 432],
    ['CAN', '2020-08-01', 13232, 2324, 4321, 32334, 767, 432],
    ['DEU', '2020-08-01', 13232, 2324, 4321, 32334, 767, 432],
    ['AFG', '2020-08-01', 13232, 2324, 4321, 32334, 767, 432],
]
OWID_CASES_SAMPLE_COL_NAMES = [
    ['country_code', 'date', 'total_cases',
     'new_cases', 'total_deaths', 'new_deaths',
     'total_cases_per_million', 'total_deaths_per_million'] for _ in OWID_CASES_SAMPLE_DATA
]
OWID_COUNTRIES_SAMPLE_DATA = [
    ['North America', 'United States of America', 38928341.0, 54.422, 2.581, 1.337, 1803.987, 'USA'],
    ['North America', 'Canada', 2877800.0, 104.871, 13.188, 8.643, 11803.431, 'CAN'],
    ['Europe', 'Germany', 43851043.0, 17.348, 6.211, 3.857, 13913.839, 'DEU'],
    ['Asia', 'Afghanistan', 32866268.0, 23.89, 2.405, 1.362, 5819.495, 'AFG']
]
OWID_COUNTRIES_SAMPLE_COL_NAMES = [
    ['continent', 'location', 'population',
     'population_density', 'aged_65_older',
     'aged_70_older', 'gdp_per_capita', 'country_code'] for _ in OWID_COUNTRIES_SAMPLE_DATA
]
for db in DB_LIST:
    db.drop_tables()
    db.create_tables(config.TABLES)
    db.insert_into_table(config.COUNTRY_INFO_TABLE, OWID_COUNTRIES_SAMPLE_COL_NAMES, OWID_COUNTRIES_SAMPLE_DATA)
    db.insert_into_table(config.COVID_BY_COUNTRY_TABLE, OWID_CASES_SAMPLE_COL_NAMES, OWID_CASES_SAMPLE_DATA)
