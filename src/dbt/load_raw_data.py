import os
import json
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Helper function to safely access nested dictionary fields
def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d

# Directory with raw JSON files
RAW_DATA_DIR = "Data/raw/telegram_messages/"

def load_json_to_postgres():
    for date_folder in os.listdir(RAW_DATA_DIR):
        folder_path = os.path.join(RAW_DATA_DIR, date_folder)
        if not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            channel_name = file.replace(".json", "")
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    messages = json.load(f)
                    for msg in messages:
                        cur.execute("""
                            INSERT INTO raw_telegram_messages (
                                channel, message_id, message_text, date, sender_id, raw_json
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            channel_name,
                            msg.get('id'),
                            msg.get('message'),
                            msg.get('date'),
                            safe_get(msg, 'from_id', 'user_id'),
                            json.dumps(msg)
                        ))
                    print(f"Loaded {len(messages)} messages from {channel_name}")
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_json_to_postgres()