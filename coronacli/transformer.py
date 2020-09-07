from abc import ABC, abstractmethod


class Transformer(ABC):

    def __init__(self, parameters, db):
        super().__init__()
        self.parameters = parameters
        self.db = db
        self._construct_common_query_elements()

    def _filter_by(self, expression=None):
        if not expression:
            pass

        return expression

    def _construct_common_query_elements(self):
        pass

    @abstractmethod
    def transform(self):
        pass


class CountryTransformer(Transformer):

    def __init__(self, parameters, db):
        super().__init__(parameters, db)

    def transform(self):
        pass
