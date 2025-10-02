import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
from django.core.cache import cache
from .models import Song, Movie, Quote, Award, Timeline, FanVote
from django.core.exceptions import ValidationError
import logging
import requests
import random

logger = logging.getLogger(__name__)

def get_spotify_client():
    """Initialize Spotify client with credentials."""
    try:
        if not (settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET):
            logger.warning("Spotify credentials missing.")
            raise ValidationError("Spotify credentials not configured.")
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET
        ))
        return sp
    except Exception as e:
        logger.error(f"Failed to initialize Spotify client: {str(e)}")
        raise ValidationError(f"Spotify authentication failed: {str(e)}")

def enhance_song_with_spotify(song_title, movie_title, retries=3, backoff=1):
    """Search Spotify for a song and update with metadata, cached for 24 hours."""
    cache_key = f'spotify_song_{song_title.lower()}_{movie_title.lower()}'
    cached_data = cache.get(cache_key)
    if cached_data:
        Song.objects.filter(title__iexact=song_title, movie__title__iexact=movie_title).update(**cached_data)
        logger.info(f"Used cached Spotify data for '{song_title}'")
        return

    sp = get_spotify_client()
    if not sp:
        return

    query = f"track:{song_title} artist:\"{movie_title}\" SRK"
    for attempt in range(retries):
        try:
            results = sp.search(q=query, type='track', limit=1)
            tracks = results.get('tracks', {}).get('items', [])
            if tracks:
                track = tracks[0]
                data = {
                    'spotify_id': track['id'],
                    'preview_url': track.get('preview_url', ''),
                    'popularity': track.get('popularity', 0),
                    'duration': track['duration_ms'] // 1000
                }
                Song.objects.filter(title__iexact=song_title, movie__title__iexact=movie_title).update(**data)
                cache.set(cache_key, data, timeout=86400)  # Cache for 24 hours
                logger.info(f"Enhanced song '{song_title}' with Spotify data.")
                return
            else:
                logger.warning(f"No Spotify results for '{song_title}' in '{movie_title}'.")
                return
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                logger.warning(f"Spotify rate limit hit. Retrying in {backoff} seconds...")
                sleep(backoff)
                backoff *= 2
            else:
                logger.error(f"Spotify error for '{song_title}': {str(e)}")
                raise ValidationError(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error enhancing '{song_title}': {str(e)}")
            raise ValidationError(f"Failed to fetch Spotify data: {str(e)}")
    logger.error(f"Failed to enhance '{song_title}' after {retries} retries.")
    raise ValidationError("Spotify rate limit exceeded. Please try again later.")

def load_movies():
    """Load movies from TMDb, cached for 24 hours."""
    cache_key = 'tmdb_movies'
    movies = cache.get(cache_key)
    if movies:
        return movies
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/search/person",
            params={'api_key': settings.TMDB_API_KEY, 'query': 'Shah Rukh Khan'}
        )
        response.raise_for_status()
        data = response.json()
        movies = []
        for result in data.get('results', []):
            for movie in result.get('known_for', []):
                movie_data = {
                    'tmdb_id': movie['id'],
                    'title': movie['title'],
                    'release_year': int(movie['release_date'].split('-')[0]) if movie.get('release_date') else None,
                    'description': movie.get('overview', ''),
                    'poster_path': movie.get('poster_path', ''),
                    'rating': movie.get('vote_average', None),
                    'genres': [genre['name'] for genre in movie.get('genre_ids', [])]
                }
                movie_obj, created = Movie.objects.get_or_create(tmdb_id=movie_data['tmdb_id'], defaults=movie_data)
                movies.append(movie_obj)
        cache.set(cache_key, movies, timeout=86400)
        return movies
    except Exception as e:
        logger.error(f"Error loading TMDb movies: {str(e)}")
        return Movie.objects.all()  # Fallback to DB

# Placeholder service functions (implement as needed)
def get_movies_by_year(year):
    return Movie.objects.filter(release_year=year)

def get_movie_by_title(title):
    return Movie.objects.filter(title__iexact=title).first()

def get_top_rated_movies():
    return Movie.objects.order_by('-rating')[:10]

def get_movies_by_genre(genre):
    return Movie.objects.filter(genres__contains=[genre])

def get_random_quote():
    quotes = Quote.objects.all()
    return random.choice(quotes) if quotes else None

def get_quotes_by_movie(title):
    movie = Movie.objects.filter(title__iexact=title).first()
    return movie.quotes.all() if movie else []

def get_quotes_by_tag(tag):
    return Quote.objects.filter(tags__contains=[tag])

def get_awards():
    return Award.objects.all()

def get_awards_by_year(year):
    return Award.objects.filter(year=year)

def get_awards_by_type(award_type):
    return Award.objects.filter(type__iexact=award_type)

def get_timeline():
    return Timeline.objects.all()

def get_events_by_year(year):
    return Timeline.objects.filter(year=year)

def get_debut():
    return Timeline.objects.filter(event__icontains='debut').first()

def get_votes():
    return FanVote.objects.all()

def vote_favorite(title):
    movie = Movie.objects.filter(title__iexact=title).first()
    if movie:
        vote, created = FanVote.objects.get_or_create(movie=movie, defaults={'vote_count': 1})
        if not created:
            vote.vote_count += 1
            vote.save()
        return vote
    return None

def get_quiz():
    return {
        'question': 'Which movie features the quote "Picture abhi baaki hai mere dost"?',
        'options': ['Om Shanti Om', 'Dilwale Dulhania Le Jayenge', 'Baazigar', 'Chak De! India'],
        'answer': 'Om Shanti Om'
    }

def validate_quiz(title, answer):
    quiz = get_quiz()
    correct = title.lower() == quiz['answer'].lower() and answer.lower() == quiz['question'].lower()
    return {'correct': correct, 'message': 'Correct!' if correct else 'Incorrect, try again!'}