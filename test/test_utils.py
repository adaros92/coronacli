from coronacli import utils


def test_remove_special_characters():
    string_with_special_chars = r'\'\\thisis\'astring " with \ special\'chars'
    expected_string = 'thisisastring  with  specialchars'
    altered_string = utils.remove_special_characters(string_with_special_chars)
    assert altered_string == expected_string
    not_a_string = 123456
    assert utils.remove_special_characters(not_a_string) == not_a_string
    string_without_special_chars = 'this is   not a string with  special  chars'
    assert utils.remove_special_characters(string_without_special_chars) == string_without_special_chars


def test_get_special_character_treatment():
    behavior = 'remove'
    assert utils.get_special_character_treatment(behavior) == utils.remove_special_characters
    assert utils.get_special_character_treatment() == utils.remove_special_characters


def test_conform_db_record():
    supported_columns = ["country", "continent"]
    record_obj = {
        "record1": {"country": "usa", "continent": "North America", "year": 2020, "month": 8},
        "record2": {"country": "deu", "continent": "Europe", "language": "German"},
        "record3": {"country": "Cote d'Ivoire", "continent": "Africa"}
    }
    expected_records = [['usa', 'North America'], ['deu', "Europe"], ['Cote dIvoire', 'Africa']]
    expected_columns = [['country', 'continent'], ['country', 'continent'], ['country', 'continent']]
    record_result, column_result = utils.conform_db_record(record_obj, supported_columns)
    idx = 0
    for records, columns in zip(record_result, column_result):
        assert sorted(records) == sorted(expected_records[idx])
        assert sorted(columns) == sorted(expected_columns[idx])
        idx += 1
