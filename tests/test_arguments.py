import pytest

from coronacli import arguments
from tests import resources


def test_retrieve_arguments():
    class Args:
        countries = 'USA'
        states = 'all'
        cities = 'all'
        age_group = 'all'
        by_country = False
        by_state = False
        by_city = False
        by_age = True
        reset = True
    args = Args()

    parsed_args = arguments.retrieve_arguments(args)
    expected_result = {
        "countries": ['USA'],
        "states": ['ALL'],
        "cities": ['ALL'],
        "age_group": ['ALL'],
        "summarize_by": {
            "age": True,
            "country": False,
            "state": False,
            "city": False
        },
        "reset_db": True
    }
    assert parsed_args == expected_result

    args.by_country = True
    args.by_state = True
    args.by_city = True
    args.by_age = False
    args.states = 'fl,ny,wa,pa'
    args.cities = 'miami,new york,seattle,pittsburgh'

    parsed_args = arguments.retrieve_arguments(args)
    expected_result['states'] = ['FL', 'NY', 'WA', 'PA']
    expected_result['cities'] = ['MIAMI', 'NEW YORK', 'SEATTLE', 'PITTSBURGH']
    expected_result['summarize_by']['age'] = False
    expected_result['summarize_by']['country'] = True
    expected_result['summarize_by']['state'] = True
    expected_result['summarize_by']['city'] = True
    assert parsed_args == expected_result


def test_get_supported_countries():
    expected_supported_countries = (
        sorted([country_record[7] for country_record in resources.OWID_COUNTRIES_SAMPLE_DATA])
    )
    expected_supported_countries.insert(0, "ALL")
    for db in resources.DB_LIST:
        assert arguments.get_supported_countries(db) == expected_supported_countries


def test_validate_arguments():
    argument_map = {
        "countries": ['US', 'DEU', 'CAN'],
        "states": ['ALL'],
        "cities": ['ALL'],
        "age_group": ['ALL'],
        "summarize_by": {
            "age": True,
            "country": False,
            "state": False,
            "city": False
        },
        "reset_db": True
    }

    def raises_error(arg_map, exception):
        with pytest.raises(exception):
            arguments.validate_arguments(arg_map, resources.DB_LIST[0])

    def does_not_raise_error(arg_map):
        arguments.validate_arguments(arg_map, resources.DB_LIST[0])

    # 2-letter country code should raise error
    raises_error(argument_map, ValueError)
    # Fix it and the function should not raise any exceptions
    argument_map["countries"][0] = 'USA'
    does_not_raise_error(argument_map)
    # Unsupported countries should raise an exception
    argument_map["countries"][0] = 'MEX'
    raises_error(argument_map, ValueError)
    argument_map["countries"][0] = 'USA'
    # Only support 2-letter state codes
    argument_map["states"] = ['WAS']
    raises_error(argument_map, ValueError)
    argument_map["states"] = ['FL']
    does_not_raise_error(argument_map)
    user_inputs = ["countries", "states", "cities", "age_group"]
    # Support only upper case
    for key in user_inputs:
        argument_map[key][0] = argument_map[key][0].lower()
    raises_error(argument_map, ValueError)
    # Support only lists for user inputs
    for key in user_inputs:
        argument_map[key] = "NOT A LIST"
    raises_error(argument_map, TypeError)
