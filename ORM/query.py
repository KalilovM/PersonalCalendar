class Query:
    def __inti__(self):
        self._data = {"select": [], "from": []}

    def SELECT(self, *args):
        self._data["select"].extend(args)
        return self

    def FROM(self, *args):
        self._data["from"].extend(args)
        return self

    def _line(self, key):
        separator = ","
        return separator.join(self._data[key])

    def _lines(self):
        for key in self._data.keys():
            yield
