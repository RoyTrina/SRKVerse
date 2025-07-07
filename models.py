from pydantic import BaseModel
from typing import List

class Movie(BaseModel):
    title: str
    year: int
    director: str
    genres: List[str]
    plot: str

class Quote(BaseModel):
    quote: str
    movie: str
    year: int
