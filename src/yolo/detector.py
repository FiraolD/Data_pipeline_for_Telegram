from ultralytics import YOLO
import os
import json
import psycopg2
from dotenv import load_dotenv
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="telegram_dw",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),  # store in .env instead of hardcoding
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
except Exception as e:
    logger.error(f"Database connection error: {type(e).__name__} - {e}")
    exit(1)

# Directory where images are stored
image_dir = "Data/raw/images/"

def save_detection_to_db(channel, image_path, detections):
    try:
        timestamp = datetime.now().isoformat()

        # Modify this if message_id becomes available later
        message_id = None

        cur.execute("""
            INSERT INTO fct_image_detections (
                message_id, channel, image_path, detections, created_at
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            message_id,
            channel,
            image_path,
            json.dumps(detections),
            timestamp
        ))
        conn.commit()
        logger.info(f"Saved detection to DB: {image_path}")

    except Exception as e:
        logger.error(f"Error saving to DB: {type(e).__name__} - {e}")
        conn.rollback()

# Run inference on all images
for channel in os.listdir(image_dir):
    channel_dir = os.path.join(image_dir, channel)
    if not os.path.isdir(channel_dir):
        continue
    for image_file in os.listdir(channel_dir):
        if image_file.lower().endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(channel_dir, image_file)
            try:
                results = model(image_path)
                detections = []

                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        cls = int(box.cls)
                        label = model.names[cls]
                        conf = float(box.conf)
                        xyxy = box.xyxy.tolist()

                        detections.append({
                            "label": label,
                            "confidence": conf,
                            "bbox": xyxy
                        })

                print(f"Detected {len(detections)} objects in {image_file}")
                save_detection_to_db(channel, image_path, detections)

            except Exception as e:
                logger.error(f"Error processing {image_file}: {type(e).__name__} - {e}")
                continue

cur.close()
conn.close()


{{ config(materialized='table') }}

SELECT
    detection ->> 'label' AS object_class,
    detection ->> 'confidence' AS confidence_score,
    detection -> 'bbox' AS bounding_box,
    fid.image_path,
    fid.channel,
    fid.created_at
FROM public.fct_image_detections fid
CROSS JOIN JSONB_ARRAY_ELEMENTS(fid.detections) AS detection
WHERE detection ->> 'label' IS NOT NULL