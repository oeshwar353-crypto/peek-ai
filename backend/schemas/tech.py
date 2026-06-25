from pydantic import BaseModel
from typing import List

class TechAnalysis(BaseModel):
    device: str
    specifications: List[str]
    estimated_price: str
    alternatives: List[str]
