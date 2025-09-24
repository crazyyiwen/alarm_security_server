import json
import asyncpg
from fastapi import Request

async def save_message(thread_id: str, content: dict, request: Request = None):
    pool: asyncpg.Pool = request.app.state.pool
    async with pool.acquire() as conn:
        knowledge = await conn.fetchrow(
            """
            select thread_id from chat_history where thread_id = $1
            """,
            thread_id
        )
        if knowledge is not None:
            await conn.execute(
                """
                update chat_history set message = $1 where thread_id = $2
                """,
                json.dumps(content),
                thread_id
            )
        else:
            await conn.execute(
                """
                INSERT INTO chat_history (thread_id, message)
                VALUES ($1, $2)
                """,
                thread_id, 
                json.dumps(content)
            )

async def load_history(thread_id: str, request: Request = None):
    """Load all messages for a thread as JSON."""
    pool: asyncpg.Pool = request.app.state.pool
    async with pool.acquire() as conn:
        knowledge = await conn.fetchrow(
            """
            SELECT message FROM chat_history WHERE thread_id = $1 ORDER BY created_at
            """,
            thread_id
        )
    return knowledge
