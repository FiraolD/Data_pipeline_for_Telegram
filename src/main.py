from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Data Pipeline for Telegram is running!"}