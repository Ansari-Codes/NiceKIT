from Modals.Base import TABLES
from Modals.User import USERS
from Modals.Sessions import SESSIONS
import asyncio

async def CreateTables():
    for t in TABLES:
        await t.create()

if __name__ == "__main__":
    print("[initDB] Creating tables")
    asyncio.run(CreateTables())
    print("[initDB] DataBase Initialized!")
