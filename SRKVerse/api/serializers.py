from rest_framework import serializers
from .models import Movie, Song, Quote, Award, Timeline, FanVote, FanMessage
import mimetypes

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ('is_approved',)

class SongUploadSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(write_only=True)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_TYPES = ['audio/mpeg', 'audio/mp3', 'audio/wav']

    class Meta:
        model = Song
        fields = ('title', 'movie_title', 'composer', 'lyricist', 'audio_file', 'spotify_id', 'youtube_link', 'duration', 'is_approved')
        extra_kwargs = {
            'audio_file': {'required': True},
            'title': {'required': True},
            'movie_title': {'required': True},
            'is_approved': {'read_only': True},  # Controlled by admin
        }

    def validate_audio_file(self, value):
        mime_type, _ = mimetypes.guess_type(value.name)
        if mime_type not in self.ALLOWED_TYPES:
            raise serializers.ValidationError("Invalid file format. Only MP3 or WAV files are allowed.")
        if value.size > self.MAX_FILE_SIZE:
            raise serializers.ValidationError("File size exceeds 5MB limit.")
        return value

    def validate(self, data):
        movie_title = data.get('movie_title')
        song_title = data.get('title')
        movie = Movie.objects.filter(title__iexact=movie_title).first()
        if movie and Song.objects.filter(title__iexact=song_title, movie=movie).exists():
            raise serializers.ValidationError("Song or album already available")
        if not movie:
            raise serializers.ValidationError("Movie not found")
        return data

    def create(self, validated_data):
        movie_title = validated_data.pop('movie_title')
        movie = Movie.objects.get(title__iexact=movie_title)
        validated_data['movie'] = movie
        validated_data['is_approved'] = False  # Require admin approval
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