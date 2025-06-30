from django.db import models


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # TMDb movie ID
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    role = models.CharField(max_length=100, blank=True)
    poster_path = models.CharField(max_length=200, blank=True)  # TMDb poster path
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_year', 'title']  # Default ordering by release year and title


class Quote(models.Model):
    text = models.TextField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, null=True, blank=True)
    context = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50] + '...' if len(self.text) > 50 else self.text


class Meta:
    ordering = ['-created_at']  # Default ordering by newest quotes
