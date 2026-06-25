from pydantic import BaseModel
from typing import List, Any

class AnalysisResponse(BaseModel):
    category: str
    confidence: int
    detected_objects: List[str]
    ocr_text: str
    description: str
    analysis: Any
