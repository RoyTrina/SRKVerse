from django.db import models


class Movie(models.Model):
    objects = models.Manager()
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    rating = models.CharField(null=True, blank=True)
    genre = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tmdb_id, self.title, self.release_year, self.role, self.rating


class Meta:
    ordering = ['-release_year', 'title']


class Quote(models.Model):
    objects = models.Manager()
    text = models.TextField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50] + '...' if len(self.text) > 50 else self.text

    class Meta:
        ordering = ['-created_at']


class Award(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Fixed
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)  # Fixed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    class Meta:
        ordering = ['-year']


class Timeline(models.Model):
    objects = models.Manager()
    year = models.IntegerField()
    event = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} - {self.event}"

    class Meta:
        ordering = ['-year']


class FanVote(models.Model):
    objects = models.Manager()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Fixed
        self.vote_count = self.vote

    def __str__(self):
        return f"{self.movie.title} has {self.vote_count} votes"


class FanMessage(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.message[:50]}..."


class Song(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    composer = models.CharField(max_length=100, blank=True)
    lyricist = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.title} ({self.movie.title})"
