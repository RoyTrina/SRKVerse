from fastapi import APIRouter
from SRKVerse.api.models import Movie, Quote
from SRKVerse.api.services import load_movies, get_random_quote

shah_rukh_khan_router = APIRouter()



@shah_rukh_khan_router.get("/srk/movies", response_model=list[Movie])
def get_movies():
    return load_movies()

@shah_rukh_khan_router.get("/quotes", response_model=Quote)
def get_quotes():
    return get_random_quote()