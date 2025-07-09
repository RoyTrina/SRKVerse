import random
from pathlib import Path

import requests
from django.conf import settings

from .models import Movie, Quote, Award, Timeline, FanVote, Song
from .data.sample_data import SAMPLE_AWARDS, SAMPLE_QUOTES, SAMPLE_SONGS, SAMPLE_TIMELINE

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_movies():
    """Load Shah Rukh KHan's movies from TMDb into the database.
    """
    srk_id = 33488
    url = f"https://api.themoviedb.org/3/person/{srk_id}/movie_credits"
    params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
    try:
        response = 




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



    """Load movies from TMDb."""
    return search_srk_movies()


def load_quotes():
    """Load quotes from quotes.json into the database."""
    try:
        with open(DATA_DIR / "quotes.json", "r", encoding="utf-8") as f:
            quotes = json.load(f)
            for quote in quotes:
                movie = Movie.objects.filter(title=quote['movie']).first()
                Quote.objects.update_or_create(
                    text=quote['quote'],
                    defaults={
                        'movie': movie,
                        'context': f"From {quote['movie']} ({quote['year']})",
                        'tags': quote.get('tags', [])
                    }
                )
    except FileNotFoundError:
        print("quotes.json file not found.")

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


def load_awards():
    """Load awards from awards.json into the database."""
    try:
        with open(DATA_DIR / "awards.json", "r", encoding="utf-8") as f:
            awards = json.load(f)
            for award in awards:
                movie = Movie.objects.filter(title=award['movie']).first() if award.get('movie') else None
                Award.objects.update_or_create(
                    title=award['title'],
                    year=award['year'],
                    defaults={
                        'award': award.get('type', ''),
                        'description': award.get('description', ''),
                        'movie': movie
                    }
                )
    except FileNotFoundError:
        print("awards.json file not found, skipping")


def load_timeline():
    """Load timeline from the timeline.json into the database."""
    try:
        with open(DATA_DIR / "timeline.json", "r", encoding="utf-8") as f:
            timeline = json.load(f)
            for event in timeline:
                Timeline.objects.update_or_create(
                    year=event['year'],
                    event=event['event'],
                    defaults={
                        'description': event.get('description', '')
                    }
                )
    except FileNotFoundError:
        print("timeline.json file not found, skipping")
        timeline = [{"year": 1992, "event": "Debut in Deewana", "description": "Shah Rukh Khan's first film role"},
                    {"year": 2000, "event": "Founded Red Chillies Entertainment",
                     "description": "Production company launch"},
                    {"year": 2011, "event": "Ra.One Release", "description": "Sci-fi film release"}]
        for event in timeline:
            Timeline.objects.update_or_create(
                year=event['year'],
                event=event['event'],
                defaults={
                    'description': event.get('description', '')
                }
            )


def get_timeline():
    return Timeline.objects.all()


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