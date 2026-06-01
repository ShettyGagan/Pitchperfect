import os 
import asyncpg

_pool: asyncpg.Pool | None = None

async def get_pool()->asyncpg.Pool:
    global _pool

    if _pool is None:
        _pool=await asyncpg.create_pool(
            dsn=os.environ["DATABASE_URL"],  # e.g. postgresql://user:pass@host/db
            min_size=1,
            max_size=5,
        )
    return _pool


async def create_tables():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
             CREATE TABLE IF NOT EXISTS users (
                id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email       TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                created_at  TIMESTAMPTZ DEFAULT NOW()
            )
        """)


async def get_user_by_email(email:str)->dict|None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id::text, email, password FROM users WHERE email = $1", email
        )

        return dict(row) if row else None

async def create_user(email:str,password:str)->dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO users (email,password) VALUES ($1,$2) RETURNING id::text,email",
            email,password
        )
        return dict(row)