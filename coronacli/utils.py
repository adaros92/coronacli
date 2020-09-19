def escape_special_characters(value):
    """ Escapes special characters in argument """
    pass


def remove_special_characters(value):
    """ Remove special characters from argument

    :param value - a string containing special characters to remove
    :returns a string with special characters removed
    """
    # If not a string then just return as is
    if not isinstance(value, str):
        return value
    # \, ', ""
    chars_to_remove = {92, 39, 34}
    new_value = ""
    # Check if each character in the given string is a special character
    for char in value:
        # If not then keep it
        if ord(char) not in chars_to_remove:
            new_value += char
    return new_value


def get_special_character_treatment(behavior='remove'):
    """ Provides the correct utility function for desired special character parsing

    :param behavior - the desired operation to perform on special characters
    :returns a utility function to apply to the string with special characters
    """
    return {'remove': remove_special_characters, 'escape': None}[behavior]


def _append_record(records_to_insert, col_names, supported_columns, record_col_names, record):
    if len(set(supported_columns) - set(record_col_names)) == 0:
        records_to_insert.append(record)
        col_names.append(record_col_names)


def conform_db_record(record_dict, supported_columns, behavior='remove'):
    """ Given a dictionary of record objects with column names as keys and actual data as values, this function
    will perform the desired behavior on special characters for each record and retrieve only the columns from each
    record that are supported by the DB table schemas
    :param record_dict - a dictionary containing a group of record dictionaries by some key
        example: {
            "USA": {"continent": "North America", "year": 2020, "month": 8},
            "DEU": {"continent": "Europe", "year": 2020, "month": 8, language: "German"}
        }
    :param supported_columns - a collection of columns supported by the schema for which the record_dict pertains
        example: ["continent", "year", "month"]
    :param behavior - what to do with special characters in each record
    :returns a tuple containing a list of modified record lists and the corresponding columns
        example: (
            [['North America', 2020, 8], [2020, 8, 'Europe']],
            [['continent', 'year', 'month], ['year', 'month', 'continent']]
        )
    """
    # Declare final lists that will be returned from function
    records_to_insert = []
    col_names = []
    # Retrieve the utility function to apply to special characters
    special_char_func_to_apply = get_special_character_treatment(behavior)
    # Iterate over each record
    for _, record_obj in record_dict.items():
        # Declare a list of record columns and corresponding column names to append to the master lists declared above
        record = []
        record_col_names = []
        # Iterate over each column in the record
        for key, val in record_obj.items():
            clean_key = key.lower().replace(" ", "")
            # Check to see if the column is supported
            if clean_key in supported_columns:
                # Process special characters and append the record to the record list along with its column name
                record.append(special_char_func_to_apply(val))
                record_col_names.append(clean_key)
        # Add the record and column names to the master lists only if it contains all supported columns
        _append_record(records_to_insert, col_names, supported_columns, record_col_names, record)
    return records_to_insert, col_names


def conform_nested_db_record(record_dict, supported_columns, behavior='remove', include_key=False, key_name=""):
    """ Given a dictionary of record objects with column names as keys and actual data as values, this function
    will perform the desired behavior on special characters for each record and retrieve only the columns from each
    record that are supported by the DB table schemas

    :param record_dict - a dictionary containing a group of record dictionaries by some key
        example: {
            "USA": {"continent": "North America", "year": 2020, "month": 8},
            "DEU": {"continent": "Europe", "year": 2020, "month": 8, language: "German"}
        }
    :param supported_columns - a collection of columns supported by the schema for which the record_dict pertains
        example: ["continent", "year", "month"]
    :param behavior - what to do with special characters in each record
    :returns a tuple containing a list of modified record lists and the corresponding columns
        example: (
            [['North America', 2020, 8], [2020, 8, 'Europe']],
            [['continent', 'year', 'month], ['year', 'month', 'continent']]
        )
    """
    # Declare final lists that will be returned from function
    records_to_insert = []
    col_names = []
    # Retrieve the utility function to apply to special characters
    special_char_func_to_apply = get_special_character_treatment(behavior)
    # Iterate over each record
    for record_key, records in record_dict.items():
        for record_dict in records:
            record = []
            record_col_names = []
            if include_key:
                record = [record_key]
                record_col_names = [key_name]
            for key, val in record_dict.items():
                clean_key = key.lower().replace(" ", "")
                # Check to see if the column is supported
                if clean_key in supported_columns:
                    # Process special characters and append the record to the record list along with its column name
                    record.append(special_char_func_to_apply(val))
                    record_col_names.append(clean_key)
            # Add the record and column names to the master lists only if it contains all supported columns
            _append_record(records_to_insert, col_names, supported_columns, record_col_names, record)
    return records_to_insert, col_names

