from DB.db import SQL
from Modals.Base import Table, Column, Row

class Users(Table):
    def __init__(self) -> None:
        super().__init__("users", [
            Column("id").int().primary().auto_inc(),
            Column("name").text().not_null(),
            Column("email").text().not_null(),
            Column("password").text().not_null(),
            Column("avatar").text(),
            Column("role").text().default("user"),
            Column("created_at").datetime().default("CURRENT_TIMESTAMP"),
            Column("updated_at").datetime().default("CURRENT_TIMESTAMP"),
        ])

    async def add_user(self, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO {self.name} ({columns}) VALUES ({placeholders}) RETURNING *;"
        user = await SQL(query, values, True)
        u = User.from_row(user[0])
        return u

    async def get(self, id):
        query = f"SELECT * FROM {self.name} WHERE id = ?;"
        rows = await SQL(query, (id,), fetch=True)
        if not rows: return None
        return User.from_row(rows[0])

USERS = Users()

class User(Row):
    def __init__(self,
        id=None, name=None,
        email=None, password=None,
        avatar=None, role=None,
        created_at=None, updated_at=None):
        super().__init__(USERS, 'user')
        self.user_id = id
        self.user_name = name
        self.user_email = email
        self.user_avatar = avatar
        self.user_role = role
        self.user_password = password
        self.user_created_at = created_at
        self.user_updated_at = updated_at

    @classmethod
    def from_row(cls, row):
        return cls(**row)

    def __str__(self):
        return (
            f"User("
            f"id={self.user_id}, "
            f"name='{self.user_name}', "
            f"email='{self.user_email}', "
            f"role='{self.user_role}', "
            f"avatar='{self.user_avatar}'"
            f")"
        )
    
    def print(self):
        print(self.__str__())
