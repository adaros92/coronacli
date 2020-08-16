import argparse


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


def main():
    args = _parse_command_line()
    run_parameters = _retrieve_arguments(args)

    # TODO throw excepts for option combinations that are impossible (e.g. country = de, city - ny)
    # TODO throw excepts for unsupported options (e.g. country/state/city without data)


if __name__ == "__main__":
    main()
