import aiosqlite    
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_db_connection():
    conn = None
    try:
        conn = await aiosqlite.connect("backend/database/holymind.db")

        conn.row_factory = aiosqlite.Row

        yield conn

        
    finally:
        if conn:
            await conn.close()

async def get_db():
    async with get_db_connection() as conn:
        yield conn