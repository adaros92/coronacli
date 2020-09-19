from coronacli import arguments


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
