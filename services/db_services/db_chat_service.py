import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os

from system_setup.db_connect import get_connection

def save_message(thread_id: str, content: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "select thread_id from chat_history where thread_id = %s",
        (str(thread_id),)
    )
    existing = cur.fetchone()
    if existing:
        cur.execute(
            """
            update chat_history set message = %s where thread_id = %s
            """,
            (json.dumps(content), thread_id)
        )
    else:
        cur.execute(
            """
            INSERT INTO chat_history (thread_id, message)
            VALUES (%s, %s)
            """,
            (thread_id, json.dumps(content))
        )
    conn.commit()
    cur.close()
    conn.close()

def load_history(thread_id: str):
    """Load all messages for a thread as JSON."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT message FROM chat_history WHERE thread_id = %s ORDER BY created_at",
        (thread_id)
    )
    rows = [row["message"] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return rows
