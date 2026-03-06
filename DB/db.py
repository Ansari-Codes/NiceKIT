import sqlite3 as sq
import aiosqlite as asq
from app import DEV

DATABASE = "database.sqlite"

async def INIT_DB():
    con = await asq.connect(DATABASE)
    con.row_factory = sq.Row
    return con
DB = 0
async def SQL(query, params=(), fetch=False):
    global DB
    con = await INIT_DB()
    DB += 1
    if DEV:
        print(f"[SQL - {DB}] [STARTED] {query}")
    try:
        async with con.execute(query, params) as cur:
            rows = None
            if fetch:
                print(f"[SQL - {DB}] [FETCHING]")
                rows = await cur.fetchall()
            await con.commit()
            if fetch:
                print(f"[SQL - {DB}] [FETCHED]")
                return [dict(row) for row in rows] # type:ignore
            return []
    except Exception as e:
        print("SQL ERROR:", e)
        raise
    finally:
        await con.close()
        if DEV:
            print(f"[SQL - {DB}] [DONE]")
