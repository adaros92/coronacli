from coronacli.config import INPUT_TO_DB_MAP, COUNTRY_INFO_TABLE, COVID_BY_COUNTRY_TABLE

from abc import ABC, abstractmethod


class TransformerLogic(object):

    def __init__(self, existing_logic=None):
        self.select_columns = "*"
        self.filters = "1 = 1"
        self.source_table = None
        self.group_by_columns = None

        if existing_logic:
            self._parse_logic(existing_logic)

    def _parse_logic(self, logic):
        if isinstance(logic, type(self)):
            self.select_columns = logic.select_columns
            self.filters = logic.filters
            self.source_table = logic.source_table
            self.group_by_columns = logic.group_by_columns
        else:
            raise TypeError("Expected {0} for got {1}".format(__class__, type(logic)))

    def __eq__(self, other):
        if self.__dict__ == other.__dict__ and isinstance(other, type(self)):
            return True
        return False

    @property
    def select_columns(self):
        return self.__select_columns

    @select_columns.setter
    def select_columns(self, select_columns):
        import re
        assert isinstance(select_columns, str)
        regex = re.compile('[^a-zA-Z0-9*, _]')
        assert len(regex.findall(select_columns)) == 0
        regex = re.compile('[^a-zA-Z0-9]')
        assert len(regex.sub('', select_columns)) != len(select_columns)

        select_columns = select_columns.replace(" ", "")
        if select_columns in '':
            self.__select_columns = '*'
        else:
            self.__select_columns = select_columns

    @property
    def generate(self):
        if not self.source_table:
            raise AttributeError("A source table must be provided to generate logic")
        if not self.group_by_columns:
            return "SELECT {0} FROM {1} WHERE {2}".format(self.select_columns, self.source_table, self.filters)
        return "SELECT {0} FROM {1} WHERE {2} GROUP BY {3}".format(
            self.select_columns, self.source_table, self.filters, self.group_by_columns)


class TransformerLogicBuilder(object):

    def __init__(self, existing_logic=None):
        self.logic = TransformerLogic(existing_logic)
        self._supported_comparators = {'=', 'in', 'not in', '!=', '<>', '>', '<', '<=', '>='}

    def filter_by(self, column_names, values, types, comparators):
        assert len(column_names) == len(values) == len(types) == len(comparators)
        for col, val, col_type, comparator in zip(column_names, values, types, comparators):
            if comparator not in self._supported_comparators:
                raise ValueError('{0} is not one of {1}'.format(comparator, self._supported_comparators))
            elif comparator in {'in', 'not in'} and col_type in ('String', 'Date', 'Timestamp'):
                processed_val = '({0})'.format(','.join(['{0}'.format(x) for x in val]))
            elif comparator in {'in', 'not in'}:
                processed_val = '({0})'.format(','.join(val))
            elif col_type in ('String', 'Date', 'Timestamp'):
                processed_val = '{0}'.format(val)
            else:
                processed_val = val

            self.logic.filters += "and {0} {1} {2}".format(col, comparator, processed_val)

    def select_from(self, table_name, alias=None):
        processed_table_name = table_name
        if alias:
            processed_table_name += "as {0}".format(alias.replace(" ", ""))
        self.logic.source_table = processed_table_name


class Transformer(ABC):

    def __init__(self, parameters, db):
        super().__init__()
        self.parameters = parameters
        self.expected_parameters = [*INPUT_TO_DB_MAP]
        self._check_input()
        self.db = db
        self.logic = None
        self._construct_common_query_elements()

    def _construct_common_query_elements(self):
        builder = TransformerLogicBuilder(self.logic)
        column_names, values, types, comparators = [], [], [], []
        for parameter in self.expected_parameters:
            val = self.parameters.get(parameter, "")
            if val != 'all' and val != ['all']:
                # Get the corresponding column name and type in the DB for the expected parameter to filter
                column_info = INPUT_TO_DB_MAP[parameter]
                column_names.append(column_info[0])
                types.append(column_info[1])
                comparators.append('in')
        builder.filter_by(column_names, values, types, comparators)
        self.logic = builder.logic

    def _check_input(self):
        for parameter in self.expected_parameters:
            if parameter not in self.parameters:
                raise ValueError("{0} expects {1} to be provided via parameters".format(__class__, parameter))

    @abstractmethod
    def transform(self):
        pass


class CountryTransformer(Transformer):

    def __init__(self, parameters, db):
        super().__init__(parameters, db)
        self.country_demographics_table_name = COUNTRY_INFO_TABLE
        self.total_country_cases_table_name = COVID_BY_COUNTRY_TABLE

    def _get_country_data(self, table_name):
        builder = TransformerLogicBuilder(self.logic)
        builder.select_from(table_name)
        logic = builder.logic.generate
        return self.db.execute_query(logic, expect_results=True)

    def transform(self):
        # Get total cases by country
        cases = self._get_country_data(self.total_country_cases_table_name)
        print(cases)
        # Get country demographics
        demographics = self._get_country_data(self.country_demographics_table_name)
