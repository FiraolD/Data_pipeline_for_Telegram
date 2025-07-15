from fastapi import APIRouter, Depends, HTTPException
import os
import psycopg2
from pydantic import BaseModel
from typing import List

# Define router
router = APIRouter(prefix="/api")

# Pydantic model for message search
class MessageSearchResult(BaseModel):
    message: str
    channel: str
    date: str

# DB Connection
def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Message Search Endpoint
@router.get("/search/messages")
def search_messages(query: str, conn: psycopg2.extensions.connection = Depends(get_db)):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT message_text, channel, message_date
            FROM fct_messages
            WHERE message_text ILIKE %s
            LIMIT 10;
        """, (f"%{query}%",))
        result = cur.fetchall()
        cur.close()
        return [{"message": row[0], "channel": row[1], "date": str(row[2])} for row in result]
    except Exception as e:
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))