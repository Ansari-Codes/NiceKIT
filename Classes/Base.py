from DB.db import SQL
from typing import Literal, List, Any, Dict
from app import DEV
from Core.utils import escsql, randomstr, rnd

COL_TYPES = ["DATETIME", "INTEGER", "TEXT"]
TABLES = []
class SQLErr(Exception):
    pass

class Column:
    def __init__(self, name) -> None:
        self.name = name.strip().lower()
        self._sql = [f"{self.name}"]
        self.required = False
        self.unique_ = False
        self.type_ = None

    def unique(self):
        if 'UNIQUE' in self._sql: return self
        self._sql.append("UNIQUE")
        self.unique_ = True
        return self

    def not_null(self):
        if 'NOT NULL' in self._sql: return self
        self._sql.append("NOT NULL")
        self.required = True
        return self
    
    def type(self, type: Literal["DATETIME", "INTEGER", "TEXT"]):
        if type in self._sql: return self
        self._sql.append(type.upper().strip())
        self.type_ = type
        return self
    
    def text(self):
        return self.type("TEXT")
    
    def int(self):
        return self.type("INTEGER")
    
    def datetime(self):
        return self.type("DATETIME")

    def default(self, default):
        for i in self._sql:
            if i.startswith("DEFAULT"): return self
        if default == "CURRENT_TIMESTAMP": self._sql.append("DEFAULT CURRENT_TIMESTAMP")
        else: self._sql.append(f"DEFAULT '{escsql(default)}'")
        return self

    def refrences(self, ref_tb, ref_col):
        for i in self._sql:
            if i.startswith("REFERENCES"): return self
        self._sql.append(f"REFERENCES {ref_tb}({ref_col})")
        return self

    def primary(self):
        if "PRIMARY KEY" in self._sql: return self
        self._sql.append("PRIMARY KEY")
        return self

    def auto_inc(self):
        if "AUTOINCREMENT" in self._sql: return self
        self._sql.append("AUTOINCREMENT")
        return self
    
    def __sql__(self):
        return " ".join(self._sql)

    def print(self):
        print(self.__sql__())

class Table:
    def __init__(self, name, columns: List[Column]) -> None:
        self.name = name.strip().lower()
        if self.name in [t.name for t in TABLES]:
            raise SQLErr(f"Table with name `{self.name}` already exists in TABLES!")
        self.columns = columns
        TABLES.append(self)

    def __sql__(self):
        sql = ',\n\t'.join([c.__sql__() for c in self.columns])
        return f"""CREATE TABLE IF NOT EXISTS {self.name} (\n\t{sql}\n);"""

    async def is_unique(self, item, field: str):
        col = next((c for c in self.columns if c.name == field), None)
        if not col:
            raise SQLErr(f"Column '{field}' does not exist in table '{self.name}'")
        if not col.unique_:
            raise SQLErr(f"Column '{field}' is not marked UNIQUE")
        query = f"SELECT 1 FROM {self.name} WHERE {field} = ? LIMIT 1;"
        rows = await SQL(query, (item,), fetch=True)
        return len(rows) == 0

    async def create(self):
        if DEV: print(f"Creating {self.name}!")
        await SQL(self.__sql__())
        if DEV: print(f"Created {self.name}!")

    async def drop(self):
        if DEV: print(f"Dropping {self.name}!")
        await SQL(f"DROP TABLE IF EXISTS {self.name};")
        if DEV: print(f"Dropped {self.name}!")

    async def clear(self):
        if DEV: print(f"Clearing {self.name}!")
        await SQL(f"DELETE FROM `{self.name}`;")
        if DEV: print(f"Cleared {self.name}!")

    def print(self):
        print(self.__sql__())

class Row:
    def __init__(self, table, field_prefix=None, **data):
        self.table = table
        self.field_prefix = field_prefix

        for k, v in data.items():
            setattr(self, k, v)

    def _prefix(self):
        if self.field_prefix:
            return f"{self.field_prefix}_"
        return f"{self.table.name}_"

    def _pk_attr(self):
        return f"{self._prefix()}id"

    def _col(self, attr):
        prefix = self._prefix()
        if attr.startswith(prefix):
            return attr[len(prefix):]
        return attr

    async def update(self, **kwargs):
        set_parts = []
        params = []

        for attr, value in kwargs.items():
            column = self._col(attr)
            set_parts.append(f"{column}=?")
            params.append(value)
            setattr(self, attr, value)

        set_clause = ", ".join(set_parts)

        pk_attr = self._pk_attr()
        pk_val = getattr(self, pk_attr)

        params.append(pk_val)

        sql = f"""
        UPDATE {self.table.name}
        SET {set_clause}
        WHERE id=?
        """

        return await SQL(sql, tuple(params), fetch=False)

    async def delete(self):
        pk_attr = self._pk_attr()
        pk_val = getattr(self, pk_attr)

        sql = f"""
        DELETE FROM {self.table.name}
        WHERE id=?
        """

        return await SQL(sql, (pk_val,), fetch=False)

    def get_dict(self):
        prefix = self._prefix()
        result = {}

        for k, v in self.__dict__.items():
            if k.startswith(prefix):
                result[self._col(k)] = v

        return result

class Variable:
    def __init__(self, value, name=None, on_change=None):
        self.value = value
        self._name = name
        self._group = None
        self._on_change = on_change or (lambda x: x)

    def set(self, value):
        self.value = value
        return self._on_change(self.value)

    def on_change(self, func):
        self._on_change = func

    @property
    def name(self):
        return self._name

    def set_name(self, n):
        self._name = n

    @property
    def group(self):
        return self._group
    
    def __str__(self):
        return f"{self._name}({self.value})"

    def __repr__(self):
        return str(self)

class VGroup:
    def __init__(self, name=None):
        self._name = name or "group"
        self._variables = {}

    @property
    def group_name(self):
        return self._name

    def add_var(self, var: Variable):
        name = var.name

        if name is None:
            name = f"v{len(self._variables)}"
            var.set_name(name)

        if name in self._variables:
            raise Exception(
                f"VGroup('{self._name}') already contains variable '{name}'"
            )

        var._group = self # type:ignore
        self._variables[name] = var

        return self

    def remove_var(self, name):
        if name not in self._variables:
            raise Exception(
                f"VGroup('{self._name}') has no variable '{name}'"
            )

        var = self._variables.pop(name)
        var._group = None
        return self

    def __getattr__(self, item):
        if item in self._variables:
            return self._variables[item]
        raise AttributeError(f"{self._name} has no variable '{item}'")

    def __str__(self):
        vars_str = ", ".join(str(v) for v in self._variables.values())
        return f"{self._name}({vars_str})"

class Response:
    def __init__(self, response:None | List | Dict | Any = None, errors:None|dict=None) -> None:
        self.response = response or {}
        self.errors = errors or {}
    
    @property
    def success(self):
        return not (self.errors and all([bool(v) for v in self.errors.values()]))

    def __str__(self) -> str:
        return f"""
-----------
SUCCESS:\n\t{self.success}\nERROR:\n\t{self.errors}\nRESPONSE: \n\t{self.response}
-----------
    """
