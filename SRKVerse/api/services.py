# SRKVerse/api/services.py
import requests
from django.conf import settings
from .models import Movie, Quote
from random import choice

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"

def search_srk_movies():
    """Fetch Shah Rukh Khan movies from TMDb and store in database."""
    srk_id = 33488  # Shah Rukh Khan's TMDb person_id
    url = f"{BASE_URL}/person/{srk_id}/movie_credits"
    params = {"api_key": API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        movies = response.json().get("cast", [])
        for movie in movies:
            release_date = movie.get('release_date', '')
            release_year = int(release_date[:4]) if release_date else None
            Movie.objects.update_or_create(
                tmdb_id=movie['id'],
                defaults={
                    'title': movie.get('title', ''),
                    'release_year': release_year,
                    'description': movie.get('overview', ''),
                    'role': movie.get('character', ''),
                    'poster_path': movie.get('poster_path', '')
                }
            )
        return Movie.objects.all()
    except requests.RequestException as e:
        print(f"Error fetching TMDb movies: {e}")
        return Movie.objects.all()

def load_movies():
    """Load movies from TMDb."""
    return search_srk_movies()

def get_random_quote():
    """Return a random quote from the database."""
    quotes = Quote.objects.all()
    return choice(quotes) if quotes else None

def load_quotes():
    """Load hardcoded quotes into the database."""
    quotes = [
        {"quote": "Don’t underestimate the power of a common man.", "movie": "Chennai Express", "year": 2013},
        {"quote": "Kabhi kabhi jeetne ke liye kuch haarna padta hai.", "movie": "Baazigar", "year": 1993},
        {"quote": "Picture abhi baaki hai mere dost.", "movie": "Om Shanti Om", "year": 2007}
    ]
    for quote in quotes:
        movie = Movie.objects.filter(title=quote['movie']).first()
        Quote.objects.update_or_create(
            text=quote['quote'],
            defaults={
                'movie': movie,
                'context': f"From {quote['movie']} ({quote['year']})"
            }
        )