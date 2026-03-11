from Classes.Base import TABLES
import asyncio
# The table class below should be imported to register all the tables
import Classes.Tables

async def CreateTables():
    for t in TABLES:
        await t.create()

if __name__ == "__main__":
    print("[initDB] Creating tables")
    asyncio.run(CreateTables())
    print("[initDB] DataBase Initialized!")
