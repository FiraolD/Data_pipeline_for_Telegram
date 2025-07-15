import os
from pydantic import BaseModel
from typing import Optional

class ProductDetection(BaseModel):
    product: str
    confidence: float

class ImageDetectionsResponse(BaseModel):
    message_id: int
    image_path: str
    detections: list[ProductDetection]