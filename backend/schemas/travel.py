from pydantic import BaseModel
from typing import List

class TravelAnalysis(BaseModel):
    destination: str
    hotels: List[str]
    budget: str
    things_to_do: List[str]
