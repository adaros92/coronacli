import pytest

from coronacli import transformer


def test_default_transformer_logic():
    logic = transformer.TransformerLogic()
    # Default behavior should throw error because no table name provided
    with pytest.raises(AttributeError):
        _ = logic.generate
    # When table is provided it should select all records
    logic.source_table = "SomeTable"
    expected_logic = "SELECT * FROM SomeTable WHERE 1 = 1"
    received_logic = logic.generate
    assert received_logic == expected_logic


def test_select_transformer_logic():
    logic = transformer.TransformerLogic()
    logic.source_table = "SomeTable"
    logic.select_columns = "column_a,    column_b,  column_c"
    expected_logic = "SELECT column_a,column_b,column_c FROM SomeTable WHERE 1 = 1"
    received_logic = logic.generate
    assert received_logic == expected_logic
    bad_columns = ["13232\\x&*", '1', '-2412', '-=+']
    for col in bad_columns:
        with pytest.raises(AssertionError):
            logic.select_columns = col
