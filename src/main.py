from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
import os
import psycopg2
from dotenv import load_dotenv
router = APIRouter()

from src.api.products import router as products_router
from src.api.channels import router as channels_router
from src.api.messages import router as messages_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Telegram Analytics API")
# Include routers
app.include_router(products_router)
app.include_router(channels_router)
app.include_router(messages_router)

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

# Sample response model
class ProductCount(BaseModel):
    product: str
    count: int

@app.get("/")
def read_root():
    return {"message": "Welcome to Telegram Data Pipeline API"}


# src/main.py

