from sqlalchemy import Column, Integer, String, Numeric

DBNAME = 'coronadb'
SQLITE = 'sqlite'
TABLES = {
    'owid_covid_data': {
        'table_name': 'owid_covid_data',
        'schema': [
        {'col_name': 'country_code', 'col_obj': Column('country_code', String)},
        {'col_name': 'date', 'col_obj': Column('date', String)},
        {'col_name': 'total_cases', 'col_obj': Column('total_cases', Integer)},
        {'col_name': 'new_cases', 'col_obj': Column('new_cases', Integer)},
        {'col_name': 'total_deaths', 'col_obj': Column('total_deaths', Integer)},
        {'col_name': 'new_deaths', 'col_obj': Column('new_deaths', Integer)},
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
OWID_DATA_URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json"
COUNTRY_INFO_TABLE = "owid_country_data"
COVID_BY_COUNTRY_TABLE = "owid_covid_data"
COUNTRY_SCRAPER_NAME = "OurWorldInData"
