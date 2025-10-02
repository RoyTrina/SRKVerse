from django.contrib import admin
from .models import Movie, Song, Quote, Award, Timeline, FanVote, FanMessage

# Register your models here.

# Custom admin class for Movie
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating', 'role', 'genres_display')
    list_filter = ('release_year', 'genres')
    search_fields = ('title', 'description', 'role')
    readonly_fields = ('tmdb_id',)  # Prevent editing TMDb ID
    fieldsets = (
        (None, {'fields': ('tmdb_id', 'title', 'release_year', 'description')}),
        ('Details', {'fields': ('role', 'poster_path', 'rating', 'genres')}),
    )

    def genres_display(self, obj):
        return ", ".join(obj.genres)
    genres_display.short_description = 'Genres'

# Custom admin class for Song
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'composer', 'lyricist', 'duration')
    list_filter = ('movie',)
    search_fields = ('title', 'composer', 'lyricist', 'movie__title')
    fieldsets = (
        (None, {'fields': ('title', 'movie')}),
        ('Metadata', {'fields': ('composer', 'lyricist', 'duration')}),
        ('Media', {'fields': ('audio_file', 'spotify_id', 'youtube_link')}),
    )
    # Ensure audio_file uploads work; requires proper media settings
    def save_model(self, request, obj, form, change):
        # Handle file uploads (stored locally or on S3 in production)
        super().save_model(request, obj, form, change)

# Custom admin class for Quote
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'movie', 'tags_display')
    list_filter = ('movie', 'tags')
    search_fields = ('text', 'context', 'movie__title')
    fieldsets = (
        (None, {'fields': ('text', 'movie')}),
        ('Details', {'fields': ('context', 'tags')}),
    )

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Quote'

    def tags_display(self, obj):
        return ", ".join(obj.tags)
    tags_display.short_description = 'Tags'

# Custom admin class for Award
@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'type', 'movie', 'description_preview')
    list_filter = ('year', 'type', 'movie')
    search_fields = ('title', 'description', 'movie__title')
    fieldsets = (
        (None, {'fields': ('title', 'year', 'type')}),
        ('Details', {'fields': ('description', 'movie')}),
    )

    def description_preview(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_preview.short_description = 'Description'

# Custom admin class for Timeline
@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('event', 'year', 'description_preview')
    list_filter = ('year',)
    search_fields = ('event', 'description')
    fieldsets = (
        (None, {'fields': ('year', 'event')}),
        ('Details', {'fields': ('description',)}),
    )

    def description_preview(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
    description_preview.short_description = 'Description'

# Custom admin class for FanVote
@admin.register(FanVote)
class FanVoteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'vote_count')
    list_filter = ('movie',)
    search_fields = ('movie__title',)
    readonly_fields = ('vote_count',)  # Prevent manual vote count edits

# Custom admin class for FanMessage
@admin.register(FanMessage)
class FanMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'message')
    readonly_fields = ('created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_preview.short_description = 'Message'