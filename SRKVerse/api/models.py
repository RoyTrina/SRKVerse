from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=100, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(null=True, blank=True)
    genres = models.JSONField(default=list)

    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, related_name='songs', on_delete=models.CASCADE)
    composer = models.CharField(max_length=100, blank=True)
    lyricist = models.CharField(max_length=100, blank=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    spotify_id = models.CharField(max_length=255, blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    preview_url = models.URLField(blank=True, null=True)
    popularity = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # In seconds
    is_approved = models.BooleanField(default=False)  # Admin approval for user uploads

    class Meta:
        unique_together = ('title', 'movie')

    def __str__(self):
        return f"{self.title} - {self.movie.title}"

class Quote(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, related_name='quotes', on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField(blank=True)
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.text

class Award(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    movie = models.ForeignKey(Movie, related_name='awards', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

class Timeline(models.Model):
    year = models.IntegerField()
    event = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event} ({self.year})"

class FanVote(models.Model):
    movie = models.ForeignKey(Movie, related_name='fan_votes', on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.movie.title}: {self.vote_count} votes"

class FanMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.message}"