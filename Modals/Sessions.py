from DB.db import SQL
from Modals.Base import Table, Column, Row

class Sessions(Table):
    def __init__(self) -> None:
        super().__init__("sessions", [
            Column("id").int().primary().auto_inc(),
            Column("user").int().not_null().refrences('users', 'id'),
            Column("session_token").text().unique().not_null(),
            Column("expires_at").int().not_null(),
            Column("created_at").datetime().default("CURRENT_TIMESTAMP"),
        ])

SESSIONS = Sessions()

class Session(Row):
    def __init__(self,
        id=None, user=None,
        session_token=None, created_at=None,
        expires_at=None):
        super().__init__(SESSIONS)
        self.session_id = id
        self.session_user = user
        self.session_session_token = session_token
        self.session_created_at = created_at
        self.session_expires_at = expires_at
