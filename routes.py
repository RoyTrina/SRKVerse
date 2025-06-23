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

@shah_rukh_khan_router.get("/movies", response_model=list[Movie])
def get_movies():
    return load_movies()

@shah_rukh_khan_router.get("/quotes", response_model=Quote)
def get_quotes():
    return get_random_quote()