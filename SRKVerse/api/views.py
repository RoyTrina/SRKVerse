from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Quote
from .serializers import MovieSerializer, QuoteSerializer, AwardSerializer, TimelineSerializer, FanVoteSerializer, FanMessageSerializer
from .services import (load_movies, get_random_quote, get_movie_by_title,
                       get_movies_by_year, get_debut,
                       get_top_rated, get_movies_by_genre, get_quotes_by_movie, get_quotes_by_tag, get_awards,
                       get_awards_by_year, get_awards_by_type, get_events_by_year, get_timeline, get_votes,
                       vote_favorite, get_quiz, validate_quiz, submit_message)


@api_view(['GET'])
def get_all_movies():
    movies = load_movies()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movies_by_year_view(year: int):
    movies = get_movies_by_year(year)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_by_title_view(title: str):
    movie = get_movie_by_title(title)
    if not movie:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
def get_top_rated_view():
    movies = get_top_rated()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_by_genre_view(genre: str):
    movies = get_movies_by_genre(genre)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_quotes():
    quotes = Quote.objects.all()
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_random_quote_view():
    quote = get_random_quote()
    if not quote:
        return Response({'error': 'No quotes found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = QuoteSerializer(quote)
    return Response(serializer.data)


@api_view(['GET'])
def get_quotes_by_movie_view(title: str):
    quotes = get_quotes_by_movie(title)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_quotes_by_tag_view(tag: str):
    quotes = get_quotes_by_tag(tag)
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_awards():
    awards = get_awards()
    serializer = AwardSerializer(awards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_awards_by_year_view(year: int):
    awards = get_awards_by_year(year)
    serializer = AwardSerializer(awards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_awards_by_type_view(award_type: str):
    awards = get_awards_by_type(award_type)
    serializer = AwardSerializer(awards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_timeline_view():
    timeline = get_timeline()
    serializer = TimelineSerializer(timeline, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_events_by_year_view(year: int):
    events = get_events_by_year(year)
    serializer = TimelineSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_debut_view():
    debut = get_debut()
    if not debut:
        return Response({"error": "Debut not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = TimelineSerializer(debut)
    return Response(serializer.data)


# Fan interaction stubs (to be implemented with proper models if needed)


@api_view(['GET'])
def get_votes_view():
    votes = get_votes()
    serializer = FanVoteSerializer(votes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def vote_favorite_view(request):
    title = request.data.get('title')
    if not title:
        return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
    vote = vote_favorite(title)
    if vote:
        serializer = FanVoteSerializer(vote)
        return Response(serializer.data)
    return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_quiz_view():
    quiz = get_quiz()
    return Response(quiz)


@api_view(['POST'])
def validate_quiz_view(request):
    title = request.data.get('title')
    answer = request.data.get('answer')
    if not (title and answer):
        return Response({"error": "Title and answer are required"}, status=status.HTTP_400_BAD_REQUEST)
    result = validate_quiz(title, answer)
    return Response(result)


@api_view(['POST'])
def submit_message_view(request):
    serializer = FanMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": f"Thank you {serializer.data['name']} for your message!"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
