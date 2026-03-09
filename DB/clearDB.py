from Classes.Base import TABLES
from Classes.Users import USERS
from Classes.Sessions import SESSIONS
import asyncio

async def CreateTables():
    for t in TABLES:
        await t.clear()

if __name__ == "__main__":
    print("[initDB] Creating tables")
    asyncio.run(CreateTables())
    print("[initDB] DataBase Initialized!")
