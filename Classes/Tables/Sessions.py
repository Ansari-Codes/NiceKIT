from datetime import datetime
from DB.db import SQL
from Classes.Base import Table, Column, Row, Response

class Sessions(Table):
    def __init__(self) -> None:
        super().__init__("sessions", [
            Column("id").int().primary().auto_inc(),
            Column("user").int().not_null().refrences('users', 'id'),
            Column("token").text().unique().not_null(),
            Column("expires_at").int().not_null(),
            Column("created_at").datetime().default("CURRENT_TIMESTAMP"),
        ])
    
    async def add_token(self, **kwargs):
        result = Response()
        for col in self.columns:
            if col.required and col.name not in kwargs:
                result.errors[col.name] = "Field is required."
        if not result.success:return result
        for col in self.columns:
            if col.unique_ and col.name in kwargs:
                if not await self.is_unique(kwargs[col.name], col.name):
                    result.errors[col.name] = "Value already exists."
        if not result.success:
            return result
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"""
        INSERT INTO {self.name} ({columns})
        VALUES ({placeholders})
        RETURNING *;
        """
        rows = await SQL(query, values, fetch=True)
        if not rows:
            result.errors["database"] = "Insert failed."
            return result
        result.response = Session.from_row(rows[0])
        return result
    
    async def get_session(self, token_or_id):
        result = Response()
        if isinstance(token_or_id, int): query = f"SELECT * FROM {self.name} WHERE id = ?;"
        else: query = f"SELECT * FROM {self.name} WHERE token = ?;"
        rows = await SQL(query, (token_or_id,), fetch=True)
        if not rows:
            result.errors["session"] = "Session not found."
            return result
        result.response = Session.from_row(rows[0])
        return result

SESSIONS = Sessions()

class Session(Row):
    def __init__(self,
        id=None, user=None,
        token=None, created_at=None,
        expires_at=None):
        super().__init__(SESSIONS, field_prefix="session")
        self.session_id = id
        self.session_user = user
        self.session_token = token
        self.session_created_at = created_at
        self.session_expires_at = expires_at

    @classmethod
    def from_row(cls, row):
        return cls(**row)

    async def is_expired(self):
        if not self.session_expires_at: return True
        now_ts = int(datetime.now().timestamp())
        return self.session_expires_at <= now_ts

    def __str__(self):
        return (
            f"Session(id={self.session_id}, user={self.session_user}, "
            f"token='{self.session_token}', expires_at={self.session_expires_at}, "
            f"created_at='{self.session_created_at}')"
        )

    def print(self):
        print(self.__str__())