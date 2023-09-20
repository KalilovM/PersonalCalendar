from collections import OrderedDict
from ORM.manager import Manager
import datetime
from enum import Enum
from abc import ABC


class OnDelete(Enum):
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"
    NO_ACTION = "NO ACTION"
    NULL = "SET NULL"
    DEFAULT = "SET DEFAULT"


class Field:
    field_value = None

    def __init__(self, primary_key=False, null=False, default=None, unique=True):
        self.primary_key = primary_key
        self.null = null
        self.default = default
        self.unique = unique

    def _final_field_name(self):
        query = self.field_value
        if self.primary_key:
            query += " PRIMARY KEY"
        if not self.null:
            query += " NOT NULL"
        if self.unique:
            query += " UNIQUE"
        if self.default:
            query += f" DEFAULT {self.default}"
        return query

    def is_primary_key(self):
        return self.primary_key

    def __repr__(self):
        return self._final_field_name()

    def __str__(self):
        return self._final_field_name()


class ForeignKeyField(Field):
    field_value = "INTEGER"

    def __init__(self, cls: "Type['Model']", on_delete=OnDelete.NO_ACTION):
        super().__init__()
        self.on_delete = on_delete.value
        self.cls = cls

    def _final_field_name(self):
        return f"{self.field_value} REFERENCES {self.cls._model_name} ON DELETE {self.on_delete}"


class CharField(Field):
    field_value = "CHAR"

    def __init__(
        self, max_length=255, primary_key=False, null=False, default=None, unique=True
    ):
        super().__init__(primary_key, null=null, default=default, unique=unique)
        self.max_length = max_length
        self.field_value += f"({max_length})"


class IntegerField(Field):
    field_value = "INTEGER"

    def __init__(self, primary_key=False, null=False, default=None, unique=False):
        super().__init__(
            primary_key=primary_key, null=null, default=default, unique=unique
        )


class DateTimeField(Field):
    field_value = "DATETIME"

    def __init__(self, null, default, unique, primary_key=False, auto_now=False):
        super().__init__(primary_key, null=null, default=default, unique=unique)
        self.auto_now = auto_now
        if auto_now:
            self.default = datetime.datetime.now()
        else:
            self.default = None

    def __str__(self):
        return super()._final_field_name()


class MetaModel(type):
    def __new__(mcs, class_name, parents, attributes: dict):
        fields = OrderedDict()
        for k, v in attributes.items():
            if isinstance(v, Field):
                fields[k] = v
                attributes[k] = None
        c = super(MetaModel, mcs).__new__(mcs, class_name, parents, attributes)
        c._model_name = attributes["__qualname__"].lower()
        c._original_fields = fields
        c.objects = Manager(c)
        return c


class Model(metaclass=MetaModel):
    def __init__(self, **kwargs):
        """
        Setting value to model attributes on init
        """
        self.seperator = " ,"
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _attrs(self) -> dict:
        fields = {}
        for k, v in self._original_fields.items():
            if k != "id":
                fields[k] = getattr(self, k)
        return fields

    @classmethod
    def _get_fields_query(cls):
        return [
            f"{k} {v}" for k, v in cls._original_fields.items() if isinstance(v, Field)
        ]

    def __repr__(self):
        str_values = ", ".join([f"{v}" for _, v in self._attrs().items()])
        return f"{self.__class__.__name__}({str_values})"
