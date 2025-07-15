from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductDetection(BaseModel):
    product: str
    confidence: float

class ImageDetectionsResponse(BaseModel):
    message_id: int
    image_path: str
    detections: List[ProductDetection]