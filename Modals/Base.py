from DB.db import SQL
from typing import Literal, List
from app import DEV
from utils import escsql

COL_TYPES = ["DATETIME", "INTEGER", "TEXT"]
TABLES = []
class SQLErr(Exception):
    pass

class Column:
    def __init__(self, name) -> None:
        self.name = name.strip().lower()
        self._sql = [f"{self.name}"]

    def unique(self):
        if 'UNIQUE' in self._sql: return self
        self._sql.append("UNIQUE")
        return self

    def not_null(self):
        if 'NOT NULL' in self._sql: return self
        self._sql.append("NOT NULL")
        return self
    
    def type(self, type: Literal["DATETIME", "INTEGER", "TEXT"]):
        if type in self._sql: return self
        self._sql.append(type.upper().strip())
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