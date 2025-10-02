from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from .serializers import (
    MovieSerializer, SongSerializer, SongUploadSerializer, QuoteSerializer,
    AwardSerializer, TimelineSerializer, FanVoteSerializer, FanMessageSerializer
)
from .services import (
    load_movies, get_random_quote, get_movies_by_year, get_movie_by_title,
    get_top_rated_movies, get_movies_by_genre, get_quotes_by_movie,
    get_quotes_by_tag, get_awards, get_awards_by_year, get_awards_by_type,
    get_timeline, get_events_by_year, get_debut, get_votes, vote_favorite,
    get_quiz, validate_quiz, enhance_song_with_spotify
)
from .models import Song, Movie
from django.core.exceptions import ValidationError
import logging
import sentry_sdk
from django.conf import settings

logger = logging.getLogger(__name__)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_all_movies(request):
    """Fetch all movies, cached for 1 hour."""
    try:
        cache_key = 'movies_all'
        movies = cache.get(cache_key)
        if not movies:
            movies = load_movies()  # Assumes TMDb integration
            cache.set(cache_key, movies, timeout=3600)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching movies: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch movies"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_movies_by_year_view(request, year):
    """Fetch movies by release year, cached for 1 hour."""
    try:
        cache_key = f'movies_year_{year}'
        movies = cache.get(cache_key)
        if not movies:
            movies = get_movies_by_year(year)
            cache.set(cache_key, movies, timeout=3600)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching movies for year {year}: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No movies found for year {year}"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_movie_by_title_view(request, title):
    """Fetch a movie by title, cached for 1 hour."""
    try:
        cache_key = f'movie_title_{title.lower()}'
        movie = cache.get(cache_key)
        if not movie:
            movie = get_movie_by_title(title)
            cache.set(cache_key, movie, timeout=3600)
        if movie:
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching movie '{title}': {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch movie"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_top_rated_view(request):
    """Fetch top-rated movies, cached for 1 hour."""
    try:
        cache_key = 'movies_top_rated'
        movies = cache.get(cache_key)
        if not movies:
            movies = get_top_rated_movies()
            cache.set(cache_key, movies, timeout=3600)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching top-rated movies: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch top-rated movies"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_by_genre_view(request, genre):
    """Fetch movies by genre, cached for 1 hour."""
    try:
        cache_key = f'movies_genre_{genre.lower()}'
        movies = cache.get(cache_key)
        if not movies:
            movies = get_movies_by_genre(genre)
            cache.set(cache_key, movies, timeout=3600)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching movies for genre {genre}: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No movies found for genre {genre}"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_all_songs(request):
    """Fetch all approved songs, cached for 1 hour."""
    try:
        cache_key = 'songs_all'
        songs = cache.get(cache_key)
        if not songs:
            songs = Song.objects.filter(is_approved=True)
            cache.set(cache_key, songs, timeout=3600)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching songs: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch songs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_movie_songs(request, title):
    """Fetch approved songs for a movie, cached for 1 hour."""
    try:
        cache_key = f'songs_movie_{title.lower()}'
        songs = cache.get(cache_key)
        if not songs:
            movie = Movie.objects.filter(title__iexact=title).first()
            if movie:
                songs = movie.songs.filter(is_approved=True)
                cache.set(cache_key, songs, timeout=3600)
            else:
                return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching songs for movie '{title}': {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch songs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@ratelimit(key='user_or_ip', rate='5/m', method='POST')
@permission_classes([IsAuthenticated])
def upload_song(request):
    """Handle authenticated song uploads with Spotify enhancement."""
    try:
        serializer = SongUploadSerializer(data=request.data)
        if serializer.is_valid():
            song = serializer.save()
            # Attempt Spotify enhancement
            try:
                enhance_song_with_spotify(serializer.validated_data['title'], serializer.validated_data['movie_title'])
                return Response({
                    "message": "Song uploaded successfully, pending admin approval",
                    "song": serializer.data
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                logger.warning(f"Spotify enhancement failed for '{serializer.validated_data['title']}': {str(e)}")
                return Response({
                    "message": "Song uploaded successfully, pending admin approval, but Spotify metadata could not be fetched",
                    "song": serializer.data,
                    "warning": str(e)
                }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error uploading song: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to upload song"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_all_quotes(request):
    """Fetch all quotes, cached for 1 hour."""
    try:
        cache_key = 'quotes_all'
        quotes = cache.get(cache_key)
        if not quotes:
            quotes = Quote.objects.all()
            cache.set(cache_key, quotes, timeout=3600)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching quotes: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch quotes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_random_quote_view(request):
    """Fetch a random quote, cached for 10 minutes."""
    try:
        cache_key = 'random_quote'
        quote = cache.get(cache_key)
        if not quote:
            quote = get_random_quote()
            cache.set(cache_key, quote, timeout=600)
        if quote:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data)
        return Response({"error": "No quotes available"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching random quote: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch random quote"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_quotes_by_movie_view(request, title):
    """Fetch quotes by movie title, cached for 1 hour."""
    try:
        cache_key = f'quotes_movie_{title.lower()}'
        quotes = cache.get(cache_key)
        if not quotes:
            quotes = get_quotes_by_movie(title)
            cache.set(cache_key, quotes, timeout=3600)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching quotes for movie '{title}': {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No quotes found for movie '{title}'"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_quotes_by_tag_view(request, tag):
    """Fetch quotes by tag, cached for 1 hour."""
    try:
        cache_key = f'quotes_tag_{tag.lower()}'
        quotes = cache.get(cache_key)
        if not quotes:
            quotes = get_quotes_by_tag(tag)
            cache.set(cache_key, quotes, timeout=3600)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching quotes for tag '{tag}': {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No quotes found for tag '{tag}'"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_all_awards(request):
    """Fetch all awards, cached for 1 hour."""
    try:
        cache_key = 'awards_all'
        awards = cache.get(cache_key)
        if not awards:
            awards = get_awards()
            cache.set(cache_key, awards, timeout=3600)
        serializer = AwardSerializer(awards, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching awards: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch awards"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_awards_by_year_view(request, year):
    """Fetch awards by year, cached for 1 hour."""
    try:
        cache_key = f'awards_year_{year}'
        awards = cache.get(cache_key)
        if not awards:
            awards = get_awards_by_year(year)
            cache.set(cache_key, awards, timeout=3600)
        serializer = AwardSerializer(awards, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching awards for year {year}: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No awards found for year {year}"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_awards_by_type_view(request, award_type):
    """Fetch awards by type, cached for 1 hour."""
    try:
        cache_key = f'awards_type_{award_type.lower()}'
        awards = cache.get(cache_key)
        if not awards:
            awards = get_awards_by_type(award_type)
            cache.set(cache_key, awards, timeout=3600)
        serializer = AwardSerializer(awards, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching awards for type '{award_type}': {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No awards found for type '{award_type}'"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_timeline_view(request):
    """Fetch career timeline, cached for 1 hour."""
    try:
        cache_key = 'timeline'
        timeline = cache.get(cache_key)
        if not timeline:
            timeline = get_timeline()
            cache.set(cache_key, timeline, timeout=3600)
        serializer = TimelineSerializer(timeline, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching timeline: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch timeline"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_events_by_year_view(request, year):
    """Fetch timeline events by year, cached for 1 hour."""
    try:
        cache_key = f'events_year_{year}'
        events = cache.get(cache_key)
        if not events:
            events = get_events_by_year(year)
            cache.set(cache_key, events, timeout=3600)
        serializer = TimelineSerializer(events, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching events for year {year}: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": f"No events found for year {year}"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_debut_view(request):
    """Fetch SRK's debut event, cached for 1 hour."""
    try:
        cache_key = 'debut'
        debut = cache.get(cache_key)
        if not debut:
            debut = get_debut()
            cache.set(cache_key, debut, timeout=3600)
        if debut:
            serializer = TimelineSerializer(debut)
            return Response(serializer.data)
        return Response({"error": "Debut event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error fetching debut: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch debut event"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_votes_view(request):
    """Fetch fan votes, cached for 10 minutes."""
    try:
        cache_key = 'votes'
        votes = cache.get(cache_key)
        if not votes:
            votes = get_votes()
            cache.set(cache_key, votes, timeout=600)
        serializer = FanVoteSerializer(votes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching votes: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch votes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@ratelimit(key='user_or_ip', rate='10/m', method='POST')
def vote_favorite_view(request):
    """Record a vote for a favorite movie."""
    try:
        title = request.data.get('title')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        vote = vote_favorite(title)
        if vote:
            cache.delete('votes')  # Invalidate cache
            serializer = FanVoteSerializer(vote)
            return Response(serializer.data)
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error voting for movie: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to vote for movie"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@ratelimit(key='ip', rate='100/m', method='GET')
def get_quiz_view(request):
    """Fetch a quiz question."""
    try:
        quiz = get_quiz()
        return Response(quiz)
    except Exception as e:
        logger.error(f"Error fetching quiz: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to fetch quiz"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@ratelimit(key='user_or_ip', rate='10/m', method='POST')
def validate_quiz_view(request):
    """Validate a quiz answer."""
    try:
        title = request.data.get('title')
        answer = request.data.get('answer')
        if not (title and answer):
            return Response({"error": "Title and answer are required"}, status=status.HTTP_400_BAD_REQUEST)
        result = validate_quiz(title, answer)
        return Response(result)
    except Exception as e:
        logger.error(f"Error validating quiz: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to validate quiz"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@ratelimit(key='user_or_ip', rate='10/m', method='POST')
def submit_message_view(request):
    """Submit a fan message."""
    try:
        serializer = FanMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Thank you {serializer.data['name']} for your message!"})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error submitting fan message: {str(e)}")
        sentry_sdk.capture_exception(e)
        return Response({"error": "Failed to submit fan message"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)