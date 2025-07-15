from fastapi import APIRouter, Depends, HTTPException
import os
import psycopg2
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define router
router = APIRouter(prefix="/api")

# Pydantic model for response validation
class ProductCount(BaseModel):
    product: str
    count: int

# Database connection
def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Top Products Endpoint
@router.get("/reports/top-products", response_model=List[ProductCount])
def get_top_products(limit: int = 10, conn: psycopg2.extensions.connection = Depends(get_db)):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                j.value->>'label' AS product,
                COUNT(*) AS count
            FROM fct_image_detections fid
            CROSS JOIN JSONB_ARRAY_ELEMENTS(fid.detections) AS j
            GROUP BY product
            ORDER BY count DESC
            LIMIT %s;
        """, (limit,))
        result = cur.fetchall()
        cur.close()
        return [{"product": row[0], "count": row[1]} for row in result]
    except Exception as e:
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))