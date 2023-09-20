from .query import Query
from .connector import DBConnector


class Manager:
    def __init__(self, model_class):
        self.model_class = model_class
        self._model_fields = model_class._original_fields.keys()
        self.create_q = Query().CREATE(
            model_class._model_name, model_class._get_fields_query()
        )
        self.q = Query().SELECT(*self._model_fields).FROM(model_class._model_name)
        self._connector = DBConnector()

    def filter(self, *args, **kwargs):
        self.q = self.q.WHERE(*args, **kwargs)
        return self

    def fetch(self):
        q = str(self.q)
        db_results = self._connector.fetch(q)
        results = []
        for row in db_results:
            model = self.model_class()

            for field, val in zip(self._model_fields, row):
                setattr(model, field, val)

            results.append(model)
        return results

    def create_table(self):
        self._connector.execute(str(self.create_q))
