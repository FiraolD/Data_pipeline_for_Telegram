from fastapi import APIRouter, Depends, HTTPException
import os
import psycopg2
from pydantic import BaseModel
from typing import List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define router
router = APIRouter(prefix="/api/channels")

# Pydantic model for channel activity
class ChannelActivity(BaseModel):
    date: str
    messages: int

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

# Channel Activity Endpoint
@router.get("/{channel}/activity", response_model=List[ChannelActivity])
def get_channel_activity(channel: str, conn: psycopg2.extensions.connection = Depends(get_db)):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                DATE_TRUNC('day', message_date) AS day,
                COUNT(*) AS total_messages
            FROM fct_messages
            WHERE channel = %s
            GROUP BY day
            ORDER BY day DESC;
        """, (channel,))
        result = cur.fetchall()
        cur.close()
        return [{"date": str(row[0]), "messages": row[1]} for row in result]
    except Exception as e:
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))