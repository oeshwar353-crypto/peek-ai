from pydantic import BaseModel
from typing import List

class MovieAnalysis(BaseModel):
    movie_title: str
    actors: List[str]
    plot: str
    streaming_platforms: List[str]
