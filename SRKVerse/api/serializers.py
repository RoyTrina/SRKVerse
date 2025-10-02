from rest_framework import serializers
from .models import Movie, Song, Quote, Award, Timeline, FanVote, FanMessage

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Song
        fields = '__all__'

class SongUploadSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(write_only=True)  # Accept movie title instead of ID

    class Meta:
        model = Song
        fields = ('title', 'movie_title', 'composer', 'lyricist', 'audio_file', 'spotify_id', 'youtube_link', 'duration')
        extra_kwargs = {
            'audio_file': {'required': True},  # Require audio file for uploads
            'title': {'required': True},
            'movie_title': {'required': True},
        }

    def validate(self, data):
        # Check if a song with the same title and movie already exists
        movie_title = data.get('movie_title')
        song_title = data.get('title')
        movie = Movie.objects.filter(title__iexact=movie_title).first()
        if movie and Song.objects.filter(title__iexact=song_title, movie=movie).exists():
            raise serializers.ValidationError("Song or album already available")
        return data

    def create(self, validated_data):
        # Convert movie_title to movie instance
        movie_title = validated_data.pop('movie_title')
        movie = Movie.objects.filter(title__iexact=movie_title).first()
        if not movie:
            raise serializers.ValidationError("Movie not found")
        validated_data['movie'] = movie
        return Song.objects.create(**validated_data)

class QuoteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Quote
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Award
        fields = '__all__'

class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'

class FanVoteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = FanVote
        fields = '__all__'

class FanMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanMessage
        fields = '__all__'