from Classes.Base import TABLES
import asyncio
# The table class below should be imported to register all the tables
import Classes.Tables

async def ClearTables():
    for t in TABLES:
        await t.clear()

if __name__ == "__main__":
    print("[clearDB] Clearing tables")
    asyncio.run(ClearTables())
    print("[clearDB] Cleared Initialized!")
