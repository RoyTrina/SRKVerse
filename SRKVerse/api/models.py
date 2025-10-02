from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(null=True, blank=True)
    genres = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='songs')
    composer = models.CharField(max_length=255, blank=True)
    lyricist = models.CharField(max_length=255, blank=True)
    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    spotify_id = models.CharField(max_length=255, blank=True)
    youtube_link = models.URLField(blank=True)
    duration = models.IntegerField(null=True, blank=True)  # in seconds

    def __str__(self):
        return f"{self.title} - {self.movie.title}"

class Quote(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    context = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.text[:50]

class Award(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

class Timeline(models.Model):
    year = models.IntegerField()
    event = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event} ({self.year})"

class FanVote(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.movie.title}: {self.vote_count} votes"

class FanMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.message[:50]}"