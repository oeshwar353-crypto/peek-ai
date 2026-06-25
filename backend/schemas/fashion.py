from pydantic import BaseModel
from typing import List

class FashionAnalysis(BaseModel):
    estimated_style: str
    brand: str
    price_range: str
    matching_outfits: List[str]
