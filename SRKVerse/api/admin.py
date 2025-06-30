from django.contrib import admin
from django.utils.html import format_html

from .models import Movie, Quote


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'role', 'tmdb_id', 'created_at')  # Fields to display in the list view
    search_fields = ('title', 'description', 'role')  # Fields to search
    list_filter = ('release_year',)  # Filters for sidebar
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
    list_display = ('text_preview', 'movie', 'created_at')  # Custom preview for text
    search_fields = ('text', 'context')  # Search by quote text or context
    list_filter = ('movie', 'created_at')  # Filter by associated movie or date
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
