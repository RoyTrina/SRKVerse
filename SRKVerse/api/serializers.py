from rest_framework import serializers
from .models import Movie, Quote, Award, Timeline, FanVote, FanMessage


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'tmdb_id', 'title', 'release_year', 'description', 'role', 'poster_path', 'rating', 'genre']


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'text', 'movie', 'context', 'tags']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['id', 'title', 'year', 'type', 'description', 'movie']


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['id', 'year', 'event', 'description']


class FanVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanVote
        fields = ['id', 'movie', 'user', 'vote']

class FanMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']
