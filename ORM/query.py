AND = "and"
OR = "or"


class Q:
    def __init__(self, exp_type=AND, **kwargs):
        self.seperator = exp_type
        self._params = kwargs

    def __str__(self):
        kv_pairs = [f"{k} = {v}" for k, v in self._params.items()]
        return f" {self.seperator}".join(kv_pairs)

    def __bool__(self):
        return bool(self._params)


class BaseExp:
    name = None

    def add(self, *args, **kwargs):
        """
        Method to add operators
        For Select: names of columns
        For From: name of table
        """
        raise NotImplementedError()

    def definition(self):
        return self.name + "\n\t" + self.line() + "\n"

    def line(self):
        raise NotImplementedError()

    def __bool__(self):
        raise NotImplementedError()


class Where(BaseExp):
    name = "WHERE"

    def __init__(self, exp_type=AND, **kwargs):
        self._q = Q(exp_type, **kwargs)
        self._params = []

    def add(self, exp_type=AND, **kwargs):
        self._q = Q(exp_type, **kwargs)
        return self._q

    def line(self):
        return str(self._q)

    def __bool__(self):
        return bool(self._q)


class From(BaseExp):
    name = "FROM"

    def __init__(self):
        self._params = []

    def add(self, *args, **kwargs):
        self._params.extend(args)

    def line(self):
        seperator = ","
        return seperator.join(self._params)

    def __bool__(self):
        return bool(self._params)


class Create(BaseExp):
    name = "CREATE TABLE IF NOT EXISTS "

    def __init__(self):
        self._params = []

    def add(self, table_name, fields: list):
        self.name += f"{table_name} \n ("
        self._params.extend(fields)

    def line(self):
        seperator = " ,\n\t"
        seperator = seperator.join(self._params)
        seperator += "\n )"
        return seperator

    def __bool__(self):
        return bool(self._params)


class Drop(BaseExp):
    name = "DROP TABLE IF EXISTS"

    def __init__(self):
        self._params = []

    def add(self, table_name):
        self._params.append(table_name)

    def line(self):
        seperator = ""
        return seperator.join(self._params)

    def __bool__(self):
        return bool(self._params)


class Select(BaseExp):
    name = "SELECT"

    def __init__(self):
        self._params = []

    def add(self, *args, **kwargs):
        self._params.extend(args)

    def line(self):
        seperator = ","
        return seperator.join(self._params)

    def __bool__(self):
        return bool(self._params)


class Query:
    """
    Class for converting python to sqlite3
    """

    def __init__(self):
        self._data = {
            "select": Select(),
            "from": From(),
            "where": Where(),
            "create": Create(),
            "drop": Drop(),
        }

    def SELECT(self, *args):
        self._data["select"].add(*args)
        return self

    def WHERE(self, exp_type=AND, **kwargs):
        self._data["where"].add(exp_type=AND, **kwargs)
        return self

    def FROM(self, *args):
        self._data["from"].add(*args)
        return self

    def CREATE(self, table_name, fields):
        self._data["create"].add(table_name, fields)
        return self

    def DROP(self, table_name):
        self._data["drop"].add(table_name)
        return self

    def _line(self, key):
        separator = ","
        return separator.join(self._data[key])

    def _lines(self):
        for key, val in self._data.items():
            if val:
                yield val.definition()

    def __str__(self):
        return "".join(self._lines())


# q = Query()
# print(q.CREATE("Employee", ["name INT NOT NULL", "email TEXT NOT NULL"]))
