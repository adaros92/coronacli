from coronacli import db, config


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
    if len(arg_item) != required_length and arg_item != 'ALL':
        raise ValueError("{0} args must each have a length of {1} but found {2}".format(
            arg_name, required_length, arg_item))


def get_supported_countries(db):
    countries = db.execute_query(
        "SELECT DISTINCT country_code FROM {0}".format(config.COUNTRY_INFO_TABLE), expect_results=True)
    country_list = sorted([record[0] for record in countries])
    country_list.insert(0, "ALL")
    return country_list


def validate_arguments(argument_map, db):
    supported_countries = get_supported_countries(db)
    for key, val_list in argument_map.items():
        if key in ("countries", "states", "cities", "age_group"):
            for arg_item in val_list:
                expected_case = arg_item.upper()
                if arg_item != expected_case:
                    raise ValueError("Expected {0} but received {1} in {2} args".format(expected_case, arg_item, key))
                elif key == "countries":
                    _validate_length(arg_item, key, 3)
                    if arg_item not in supported_countries:
                        raise ValueError("{0} is not a supported country code: {1}".format(
                            arg_item, supported_countries))
                elif key == "states":
                    _validate_length(arg_item, key, 2)
