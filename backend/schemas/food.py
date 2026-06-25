from pydantic import BaseModel
from typing import List

class FoodAnalysis(BaseModel):
    recipe: str
    ingredients: List[str]
    calories: int
    cook_time: str
    alternative_dishes: List[str]
