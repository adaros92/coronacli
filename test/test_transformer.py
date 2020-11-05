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
    logic.select_columns = "column_a,    column_b,  column_c, column4"
    expected_logic = "SELECT column_a,column_b,column_c,column4 FROM SomeTable WHERE 1 = 1"
    received_logic = logic.generate
    assert received_logic == expected_logic
    bad_columns = ["13232\\x&*", '-2412', '-=+']
    for col in bad_columns:
        with pytest.raises(AssertionError):
            logic.select_columns = col


def test_parse_transformer_logic():
    logic_a = transformer.TransformerLogic()
    logic_a.source_table = "TableA"
    logic_b = transformer.TransformerLogic()
    logic_b.source_table = "TableB"
    logic_b.select_columns = "column_a, column_b"
    logic_b._parse_logic(logic_a)
    assert logic_a == logic_b
    for i in [1, "some_string", sum]:
        with pytest.raises(TypeError):
            logic_b._parse_logic(i)


def test_transformer_logic_equality():
    logic_a = transformer.TransformerLogic()
    logic_a.source_table = "SomeTable"
    logic_b = transformer.TransformerLogic()
    logic_b.source_table = "SomeTable"
    assert logic_a == logic_b
    logic_a.select_columns = "column_a, column_b"
    assert logic_a != logic_b
    logic_b.select_columns = logic_a.select_columns
    assert logic_a == logic_b
