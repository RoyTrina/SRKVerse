from django.contrib import admin
from django.utils.html import format_html

from .models import Movie, Quote, Award, FanMessage, Timeline, FanVote


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'role', 'tmdb_id', 'created_at')  # Fields to display in the list view
    search_fields = ('title', 'description', 'role')  # Fields to search
    list_filter = ('release_year', 'genres')  # Filters for sidebar
    ordering = ('-release_year', 'title')  # Sort by year (descending) and title
    list_per_page = 25  # Pagination
    readonly_fields = ('tmdb_id', 'created_at')  # Prevent editing TMDb ID and creation timestamp
    fieldsets = (
        (None, {
            'fields': ('tmdb_id', 'title', 'release_year', 'description', 'role', 'poster_path')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def poster_preview(self, obj):
        if obj.poster_path:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 150px;">', obj.poster_path)
        else:
            return 'No poster available'

    poster_preview.short_description = 'Poster'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'movie', 'created_at', 'context')  # Custom preview for text
    search_fields = ('text', 'context')  # Search by quote text or context
    list_filter = ('movie', 'created_at', 'tags')  # Filter by associated movie or date
    ordering = ('-created_at',)  # Sort by newest quotes
    list_per_page = 25
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('text', 'movie', 'context')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Quote'


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'award', 'movie')  # Display award title, year, type, and movie
    search_fields = ('title', 'award', 'description')  # Search by award title, type, or description
    list_filter = ('year', 'award', 'movie')  # Filter by year, type, or movie
    ordering = ('-year', 'title')  # Sort by year (descending) and title
    list_per_page = 25
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'year', 'award', 'movie', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    @staticmethod
    def movie_preview(obj):
        return obj.movie.title if obj.movie else None


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('event', 'year', 'created_at')  # Display event, year, and creation timestamp
    search_fields = ('event', 'year')  # Search by event or year
    list_filter = ('year',)  # Filter by year
    ordering = ('-year', 'event')  # Sort by year (descending) and event
    list_per_page = 25
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('event', 'year', 'description')
        })
    )

    @staticmethod
    def movie_preview(obj):
        return obj.movie.title if obj.movie else None

@admin.register(FanVote)
class FanVoteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'vote_count')  # Display movie title and number of votes
    search_fields = ('movie__title',)  # Search by movie title
    list_filter = ('created_at',)  # Filter by creation timestamp
    ordering = ('-created_at',)  # Sort by newest votes
    list_per_page = 25
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'votes')})
    )
    @staticmethod
    def movie_preview(obj):
        return obj.movie.title if obj.movie else None


@admin.register(FanMessage)
class FanMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')  # Display user, message, and creation timestamp
    search_fields = ('user', 'message')  # Search by user or message
    list_filter = ('created_at',)  # Filter by creation timestamp
    ordering = ('-created_at',)  # Sort by newest messages
    list_per_page = 25
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'message')})
        , ('Metadata', {
        'fields': ('created_at',),
        'classes': ('collapse',)
    }),)
