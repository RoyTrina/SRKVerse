from rest_framework import serializers
from .models import Movie, Quote, Award, Timeline, FanVote, FanMessage, Song


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', read_only=True)
    
    class Meta:
        model = Award
        fields = ['id', 'title', 'year', 'type', 'description', 'movie']


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['id', 'year', 'event', 'description']


class FanVoteSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', read_only=True)
    
    class Meta:
        model = FanVote
        fields = ['id', 'movie', 'user', 'vote']

class FanMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']


class SongSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', read_only=True)
    
    audio_file = serializers.FileField(required=False)

    class Meta:
        model = Song
        fields = ['title', 'movie', 'audio_file', 'composer', 'lyricist', 'duration']