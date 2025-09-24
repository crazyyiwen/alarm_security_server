import json
import asyncpg
from fastapi import Request
import psycopg2
from psycopg2.extras import RealDictCursor
import os

from models.request_models import KnowledgeRequest
from system_setup.db_connect import get_connection

async def save_knowledge(payload: KnowledgeRequest, request: Request = None):
    """Save knowledge by knowledge_id as JSON."""
    pool: asyncpg.Pool = request.app.state.pool   # get pool from FastAPI app
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            select knowledge_id from knowledge_factory where knowledge_id = $1
            """,
            payload.knowledge_id
        )
        if row is not None:
            await conn.execute(
                """
                UPDATE knowledge_factory
                SET context = $1
                WHERE knowledge_id = $2
                """,
                json.dumps(payload.context),
                payload.knowledge_id
            )
        else:
            await conn.execute(
                """
                INSERT INTO knowledge_factory
                (knowledge_id, context)
                VALUES ($1, $2)
                """,
                payload.knowledge_id,
                json.dumps(payload.context)
            )
    return "Ok"

async def load_knowledge(knowledge_id: str, request: Request = None):
    """Load knowledge by knowledge_id as JSON."""
    pool: asyncpg.Pool = request.app.state.pool   # get pool from FastAPI app
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT context FROM knowledge_factory WHERE knowledge_id = $1",
            knowledge_id
        )
    return {"knowledge_id": knowledge_id, "context": row["context"]}
