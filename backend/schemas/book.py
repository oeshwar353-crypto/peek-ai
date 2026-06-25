from pydantic import BaseModel
from typing import List

class BookAnalysis(BaseModel):
    summary: str
    author: str
    genre: str
    similar_books: List[str]
