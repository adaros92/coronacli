import argparse

from blessings import Terminal

from coronacli import db, config, scraper, utils


class TruncatedDisplay(object):
    """ Performs similar to less command in unix OS where stdout is chunked up into a set number of
    lines and user needs to provide input to continue displaying lines """
    def __init__(self, num_lines):
        self.num_lines = num_lines

    def __ror__(self, other):
        s = str(other).split("\n")
        for i in range(0, len(s), self.num_lines):
            print(*s[i: i + self.num_lines], sep="\n")
            val = input("Press <Enter> for more or <q> to quit\n")
            if val == 'q':
                exit(0)


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
        '-bc', '--by_country', action='store_true', default=True, help="report results by country")
    parser.add_argument('-bs', '--by_state', action='store_true', help="report results by state")
    parser.add_argument('-bci', '--by_city', action='store_true', help="report results by city")
    parser.add_argument('-ba', '--by_age', action='store_true', help="report results by age")

    return parser.parse_args()


def _retrieve_arguments(args):
    """ Further parses arguments from CLI based on type and constructs concise object containing
    the parameters that will dictate behavior downstream

    :param args - arguments retrieved from call to parser.parse_args as part of argparse library
    :returns dictionary containing all arguments from CLI
    """
    # Retrieve the arguments parsed from CLI
    countries = args.countries.split(",")
    states = args.states.split(",")
    cities = args.cities.split(",")
    age_group = args.age_group
    summarize_by_age_group = args.by_age
    summarize_by_country = args.by_country
    summarize_by_state = args.by_state
    summarize_by_city = args.by_city

    # Combine them all together in one object to dictate behavior downstream
    argument_map = {
        "countries": countries,
        "states": states,
        "cities": cities,
        "age_group": age_group,
        "summarize_by": {
            "age": summarize_by_age_group,
            "country": summarize_by_country,
            "state": summarize_by_state,
            "city": summarize_by_city
        }
    }
    return argument_map


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
    covid_data_values, covid_data_col_names = utils.conform_db_record(covid_data, covid_data_columns)

    return country_info_values, country_info_col_names, covid_data_values, covid_data_col_names


def _insert_into_db(db, table, col_names, values):
    # Insert the values into DB tables
    db.insert_into_table(table, col_names, values)


def main():
    args = _parse_command_line()
    run_parameters = _retrieve_arguments(args)

    # TODO throw excepts for option combinations that are impossible (e.g. country = de, city - ny)
    # TODO throw excepts for unsupported options (e.g. country/state/city without data)

    # TODO only create tables once or when user asks for reset
    # Create database to store covid case and geographical data extracted from Internet
    corona_db = db.DB(dbname=config.DBNAME)
    corona_db.create_tables()

    # Extract and insert data into DB
    print("Extracting data...")
    country_info_values, country_info_col_names, covid_data_values, covid_data_col_names = \
        _get_country_data_values(corona_db, scraper.get_scraper(config.COUNTRY_SCRAPER_NAME))
    _insert_into_db(corona_db, config.COUNTRY_INFO_TABLE, country_info_col_names, country_info_values)
    _insert_into_db(corona_db, config.COVID_BY_COUNTRY_TABLE, covid_data_col_names, covid_data_values)

    # TODO mimic this for display later
    '''
    less = TruncatedDisplay(num_lines=50)
    "\n".join([str(x) for x in range(100)]) | less'''


if __name__ == "__main__":
    main()
