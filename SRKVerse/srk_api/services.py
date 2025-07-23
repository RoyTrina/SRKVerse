import logging
import random
from pathlib import Path

import requests
import requests.packages.urllib3.util.retry
from django.conf import settings
from requests.adapters import HTTPAdapter

from .data.sample_data import SAMPLE_QUOTES, SAMPLE_AWARDS, SAMPLE_TIMELINE, SAMPLE_SONGS
from .models import Movie, Quote, Award, Timeline, FanVote, Song

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

logger = logging.getLogger(__name__)


def create_session():
    session = requests.Session()
    retry = requests.packages.urllib3.util.retry.Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def load_movies():
    """Load Shah Rukh Khan's movies from TMDb into the database.
    """
    srk_id = 33488
    url = f"https://api.themoviedb.org/3/person/{srk_id}/movie_credits"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        movies = response.json().get("cast", [])
        genre_url = "https://api.themoviedb.org/3/genre/movie/list"
        genre_response = requests.get(genre_url, params=params)
        genre_response.raise_for_status()
        genre_map = {genre['id']: genre['name'] for genre in genre_response.json()['genres']}

        for movie in movies:
            Movie.objects.update_or_create(
                tmdb_id=movie.get("id"),
                defaults={
                    'title': movie.get('title', ''),
                    'release_year': movie.get('release_date', '')[:4] or None,
                    'description': movie.get('overview', ''),
                    'role': movie.get('character', ''),
                    'poster_path': movie.get('poster_path', ''),
                    'rating': movie.get('vote_average', 0.0),
                    'genres': [genre_map.get(gid, str(gid)) for gid in movie.get('genre_ids', [])]
                }
            )
    except requests.RequestException as e:
        logger.error(f"Error fetching TMDb movies: {e}")
        raise


def load_quotes():
    """Load quotes into the database from sampling data."""
    for q in SAMPLE_QUOTES:
        movie = Movie.objects.filter(title=q["movie"]).first()
        Quote.objects.update_or_create(
            text=q["quote"],
            defaults={
                'movie': movie,
                'year': q["year"],
                'tags': q["tags"],
                'context': q["context"]
            }
        )

        # Fall back if quotes.json is not found
    quotes = [
        {"quote": "Don’t underestimate the power of a common man.", "movie": "Chennai Express", "year": 2013,
         "tags": [], "context": "From Chennai Express (2013)"},
        {"quote": "Kabhi kabhi jeetne ke liye kuch haarna padta hai.", "movie": "Baazigar", "year": 1993, "tags": [],
         "context": "From Baazigar (1993)"},
        {"quote": "Picture abhi baaki hai mere dost.", "movie": "Om Shanti Om", "year": 2007, "tags": [],
         "context": "From Om Shanti Om (2007)"}]

    for quote in quotes:
        movie = Movie.objects.filter(title=quote['movie']).first()
        Quote.objects.update_or_create(
            text=quote['quote'],
            defaults={
                'movie': movie,
                'context': f"From {quote['movie']} ({quote['year']})",
                'tags': quote['tags']
            }
        )


def load_awards():
    """Load awards into the database from sampling data."""
    for a in SAMPLE_AWARDS:
        movie = Movie.objects.filter(title=a["movie"]).first()
        Award.objects.update_or_create(
            title=a["title"],
            year=a["year"],
            defaults={
                'type': a["type"],
                'movie': movie,
                'description': a["description"]
            }
        )


def load_timeline():
    """Load timeline events into the database from sampling data."""
    for t in SAMPLE_TIMELINE:
        Timeline.objects.update_or_create(
            year=t["year"],
            event=t["event"],
            defaults={'description': t["description"]}
        )


def load_songs():
    """Load songs into the database from sampling data."""
    for song in SAMPLE_SONGS:
        movie = Movie.objects.filter(title=song["movie"]).first()
        if movie:
            Song.objects.update_or_create(
                title=song["title"],
                movie=movie,
                defaults={
                    'artist': song.get("artist", ""),
                    'composer': song.get("composer", ""),
                    'lyricist': song.get("lyricist", ""),
                    'album': song.get("album", ""),
                    'release_year': song.get("release_year", ""),
                    'duration': song.get("duration", ""),
                    'url': song.get("url", "")
                }
            )
    movies = Movie.objects.all()
    for movie in movies:
        song = Song.objects.filter(movie=movie).first()
        if song:
            movie.song = song
            movie.save()


def get_genre_names():
    """Fetch genre names from TMDb and store in a dictionary."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return {genre['id']: genre['name'] for genre in response.json()['genres']}
    except requests.RequestException as e:
        print(f"Error fetching TMDb genre names: {e}")
        return {}


def get_random_quote():
    """Return a random quote from the database."""
    quotes = Quote.objects.all()
    return random.choice(quotes) if quotes else None


def get_movies_by_year(year: int):
    """Return movies from the database filtered by the year."""
    return Movie.objects.filter(release_year=year)


def get_movie_by_title(title: str):
    """Return a movie from the database filtered by title."""
    return Movie.objects.filter(title__iexact=title).first()


def get_top_rated():
    """Return top 10 rated movies from the database in descending order by rating."""
    return Movie.objects.filter(rating__isnull=False).order_by('-rating')[:10]


def get_movies_by_genre(genre: str):
    """Return movies from the database filtered by the genre."""
    return Movie.objects.filter(genres__icontains=genre.lower())


def get_quotes_by_movie(title: str):
    """Return quotes from the database filtered by movie title."""
    movie = Movie.objects.filter(title__iexact=title).first()
    return Quote.objects.filter(movie=movie) if movie else []


def get_quotes_by_tag(tag: str):
    """Return quotes from the database filtered by tag."""
    return Quote.objects.filter(tags__icontains=tag.lower())


def get_awards_by_year(year: int):
    """Return awards from the database filtered by the year."""
    return Award.objects.filter(year=year)


def get_awards_by_type(type: str):
    """Return awards from the database filtered by type."""
    return Award.objects.filter(award__icontains=type.lower())


def get_events_by_year(year: int):
    """Return timeline events from the database filtered by the year."""
    return Timeline.objects.filter(year=year)


def get_debut():
    """Get Shah Rukh Khan's debut event from the database."""
    return Timeline.objects.filter(event__icontains="debut").first()


def get_awards():
    """Return all the awards in the database."""
    return Award.objects.all()


def get_timeline():
    return Timeline.objects.all()


def get_votes():
    """Return all votes for favorite movies."""
    return FanVote.objects.all()


def get_quiz():
    """Return a random quiz question (example implementation)."""
    quotes = Quote.objects.all()
    if not quotes:
        return {"question": "No quotes available", "options": [], "answer": ""}
    quote = random.choice(quotes)
    movies = Movie.objects.all()[:3]
    options = [movie.title for movie in movies]
    if quote.movie and quote.movie.title not in options:
        options.append(quote.movie.title)
    random.shuffle(options)
    return {
        "question": f"Which movie is this quote from: '{quote.text}'?",
        "options": options,
        "answer": quote.movie.title if quote.movie else ""
    }


def validate_quiz(title: str, answer: str):
    """Validate a quiz answer."""
    movie = Movie.objects.filter(title__iexact=title).first()
    if not movie:
        return {"correct": False, "message": "Movie not found"}
    quotes = Quote.objects.filter(movie=movie)
    if not quotes:
        return {"correct": False, "message": "No quotes for this movie"}
    correct = any(quote.text == answer for quote in quotes)
    return {"correct": correct, "message": "Correct!" if correct else "Incorrect."}


def submit_message():
    return None


def search_srk_movies():
    """Fetch Shah Rukh Khan movies from TMDb and store in database."""
    srk_id = 33488  # Shah Rukh Khan's TMDb person_id
    url = f"{BASE_URL}/person/{srk_id}/movie_credits"
    params = {"api_key": API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        movies = response.json().get("cast", [])
        genre_map = get_genre_names()
        for movie in movies:
            release_date = movie.get('release_date', '')
            release_year = int(release_date[:4]) if release_date else None
            genre_ids = movie.get('genre_ids', [])
            genres = [genre_map.get(gid, str(gid)) for gid in
                      genre_ids]  # Note: Need more TMDb API call to fetch genre names
            Movie.objects.update_or_create(
                tmdb_id=movie['id'],
                defaults={
                    'title': movie.get('title', ''),
                    'release_year': release_year,
                    'description': movie.get('overview', ''),
                    'role': movie.get('character', ''),
                    'poster_path': movie.get('poster_path', ''),
                    'rating': movie.get('vote_average', None),
                    'genres': genres
                }
            )
        return Movie.objects.all()
    except requests.RequestException as e:
        print(f"Error fetching TMDb movies: {e}")
        return Movie.objects.all()


def vote_favorite(title: str):
    """Record a vote for a favorite movie."""
    movie = Movie.objects.filter(title__iexact=title).first()
    if not movie:
        return None
    vote, created = FanVote.objects.get_or_create(movie=movie,
                                                  defaults={'vote_count': 0})
    if not created:
        vote.votes += 1
        vote.save()
    return vote
