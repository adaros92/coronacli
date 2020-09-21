from coronacli import config


def retrieve_arguments(args):
    """ Further parses arguments from CLI based on type and constructs concise object containing
    the parameters that will dictate behavior downstream

    :param args - arguments retrieved from call to parser.parse_args as part of argparse library
    :returns dictionary containing all arguments from CLI
    """
    # Retrieve the arguments parsed from CLI
    countries = args.countries.upper().split(",")
    states = args.states.upper().split(",")
    cities = args.cities.upper().split(",")
    age_group = args.age_group.upper().split(",")
    summarize_by_age_group = args.by_age
    summarize_by_country = args.by_country
    summarize_by_state = args.by_state
    summarize_by_city = args.by_city
    reset_db = args.reset

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
        },
        "reset_db": reset_db
    }
    return argument_map


def _validate_length(arg_item, arg_name, required_length):
    """ Raises a ValueError if the length of the given argument does not match the given required length

    :param arg_item - the argument value to validate the length of
    :param arg_name - the name of the argument to validate the length of
    :param required_length - the length that the argument value must be
    """
    if len(arg_item) != required_length and arg_item != 'ALL':
        raise ValueError("{0} args must each have a length of {1} but found {2}".format(
            arg_name, required_length, arg_item))


def get_supported_countries(db):
    """ Queries the given database for a list of three-letter country codes supported by coronacli

    :param db - a database object defined in db.py
    :returns a collection of three-letter country codes
    """
    countries = db.execute_query(
        "SELECT DISTINCT country_code FROM {0}".format(config.COUNTRY_INFO_TABLE), expect_results=True)
    country_list = sorted([record[0] for record in countries])
    country_list.insert(0, "ALL")
    return country_list


def validate_arguments(argument_map, db):
    """ Performs various validation checks on the given argument_map

    :param argument_map - a dictionary of argument name to argument values defined in arguments.retrieve_arguments
    :param db - a database object to query for supported values defined in db.py
    """
    supported_countries = get_supported_countries(db)
    for key, val_list in argument_map.items():
        # Validate arguments that require text input from the user
        if key in ("countries", "states", "cities", "age_group"):
            if not isinstance(val_list, list):
                raise TypeError("Expected a list for {0} argument but received {1}", key, type(val_list))
            # Iterate over each argument value provided
            for arg_item in val_list:
                # Each argument must be capitalized (should be done in argument parsing already)
                expected_case = arg_item.upper()
                if arg_item != expected_case:
                    raise ValueError("Expected {0} but received {1} in {2} args".format(expected_case, arg_item, key))
                elif key == "countries":
                    # Countries must be three-letter country codes
                    _validate_length(arg_item, key, 3)
                    if arg_item not in supported_countries:
                        raise ValueError("{0} is not a supported country code: {1}".format(
                            arg_item, supported_countries))
                # States must be two-letter state codes
                elif key == "states":
                    _validate_length(arg_item, key, 2)
