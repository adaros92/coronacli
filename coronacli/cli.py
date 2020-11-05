import argparse

from coronacli import db, config, scraper, utils, transformer, arguments, display


def _parse_command_line():
    """ Contains main parsing logic to extract user input via the CLI """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--countries', nargs='?', default='all',
        help='comma separated list of 2-letter country codes')
    parser.add_argument(
        '-s', '--states', nargs='?', default='all',
        help='comma separated list of states/territories'
    )
    parser.add_argument(
        '-ci', '--cities', nargs='?', default='all',
        help='comma separated list of cities'
    )
    parser.add_argument(
        '-a', '--age_group', nargs=1,
        choices=['all', '0-24y', '25-34y', '35-44y', '45-54y', '55-64y', '65-74y', '75-84y', '85+y'],
        default='all', help="an age group from the allowed choices"
    )
    parser.add_argument(
        '-bc', '--by_country', action='store_true', help="report results by country")
    parser.add_argument('-bs', '--by_state', action='store_true', help="report results by state")
    parser.add_argument('-bci', '--by_city', action='store_true', help="report results by city")
    parser.add_argument('-ba', '--by_age', action='store_true', help="report results by age")
    parser.add_argument('-r', '--reset', action='store_true', help="extract new data")

    return parser.parse_args()


def _get_country_data_values(db, scraper_class):
    # Scrape the data
    scraper = scraper_class()
    covid_data, country_information = scraper.scrape()

    # Get supported columns to record in DB table
    covid_data_columns = set(db.get_column_names_from_schema(config.COVID_BY_COUNTRY_TABLE))
    country_information_columns = set(db.get_column_names_from_schema(config.COUNTRY_INFO_TABLE))

    # Construct country information values to insert into DB table
    country_info_values, country_info_col_names = utils.conform_db_record(
        country_information, country_information_columns)
    # Construct covid data values to insert into db table
    covid_data_values, covid_data_col_names = utils.conform_nested_db_record(
        covid_data, covid_data_columns, include_key=True, key_name="country_code")

    return country_info_values, country_info_col_names, covid_data_values, covid_data_col_names


def _insert_into_db(db, table, col_names, values):
    # Insert the values into DB tables
    db.insert_into_table(table, col_names, values)


def main():
    corona_db = db.DB(dbname=config.DBNAME)
    args = _parse_command_line()
    run_parameters = arguments.retrieve_arguments(args)

    # TODO throw excepts for option combinations that are impossible (e.g. country = de, city - ny)
    # TODO throw excepts for unsupported options (e.g. country/state/city without data)
    if not db.DB.db_exists(config.DBNAME, table_name_to_test=config.COVID_BY_COUNTRY_TABLE, db=corona_db) \
            or run_parameters["reset_db"]:
        # Create database to store covid case and geographical data extracted from Internet
        corona_db.drop_tables()
        corona_db.create_tables()

        # Extract and insert data into DB
        print("Extracting data...")
        country_info_values, country_info_col_names, covid_data_values, covid_data_col_names = \
            _get_country_data_values(corona_db, scraper.get_scraper(config.COUNTRY_SCRAPER_NAME))
        _insert_into_db(corona_db, config.COUNTRY_INFO_TABLE, country_info_col_names, country_info_values)
        _insert_into_db(corona_db, config.COVID_BY_COUNTRY_TABLE, covid_data_col_names, covid_data_values)

    # TODO Call factory for transformers to determine what to do; here for testing
    arguments.validate_arguments(run_parameters, corona_db)
    transform_obj = transformer.CountryTransformer(run_parameters, corona_db)
    results = transform_obj.transform()
    display_obj = display.get_display()
    display_obj(results).run()
