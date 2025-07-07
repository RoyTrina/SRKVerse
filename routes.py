from fastapi import APIRouter
from models import Movie, Quote
from services import load_movies, get_random_quote

shah_rukh_khan_router = APIRouter()


@shah_rukh_khan_router.get("/bio")
def get_srk_bio():
    return {"name": "Shah Rukh Khan",
            "nickname": "SRK, King Khan, King Of Romance",
            "born": "02-11-1965",
            "birthplace": "New Delhi, India",
            "bio": ""}
