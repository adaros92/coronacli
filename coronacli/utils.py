def escape_special_characters(value):
    if not isinstance(value, str):
        return value
    # TODO change to character ascii values
    chars_to_escape = "'\\\\n\""
    new_value = ""
    for char in value:
        if char in chars_to_escape:
            new_value += "\\{0}".format(char)
        else:
            new_value += char
    return new_value


def remove_special_characters(value):
    if not isinstance(value, str):
        return value
    # TODO change to character ascii values
    chars_to_remove = "'\\\\n\""
    new_value = ""
    for char in value:
        if char not in chars_to_remove:
            new_value += char
    return new_value


def get_special_character_treatment(behavior='remove'):
    return {'remove': remove_special_characters, 'escape': escape_special_characters}[behavior]


def conform_db_record(record_dict, supported_columns, behavior='remove'):
    records_to_insert = []
    col_names = []
    special_char_func_to_apply = get_special_character_treatment(behavior)
    for _, record_obj in record_dict.items():
        record = []
        record_col_names = []
        for key, val in record_obj.items():
            clean_key = key.lower().replace(" ", "")
            if clean_key in supported_columns:
                record.append(special_char_func_to_apply(val))
                record_col_names.append(clean_key)
        records_to_insert.append(record)
        col_names.append(record_col_names)
    return records_to_insert, col_names
