from django.db import models


class Movie(models.Model):
    objects = None
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # TMDb movie ID
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)  # TMDb poster path
    rating = models.CharField(null=True, blank=True)
    genre = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_year', 'title']  # Default ordering by release year and title


class Quote(models.Model):
    objects = None
    text = models.TextField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50] + '...' if len(self.text) > 50 else self.text

    class Meta:
        ordering = ['-created_at']  # Default ordering by newest quotes


class Award(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    type = models.CharField(max_length=100)  # e.g Filmfare, National Award, etc.
    description = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)
    movie = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    class Meta:
        ordering = ['-year']


class Timeline(models.Model):
    objects = None
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
    objects = None
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title} has {self.vote_count} votes"


class FanMessage(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.message[:50]}..."
