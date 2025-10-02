from django.contrib import admin
from .models import Movie, Song, Quote, Award, Timeline, FanVote, FanMessage

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating')
    search_fields = ('title',)
    list_filter = ('release_year', 'genres')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'movie')
    search_fields = ('title',)
    actions = ['approve_songs']

    def approve_songs(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected songs have been approved.")
    approve_songs.short_description = "Approve selected songs"

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'movie')
    search_fields = ('text',)
    list_filter = ('movie',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'type')
    list_filter = ('year', 'type')
    search_fields = ('title',)

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('event', 'year')
    list_filter = ('year',)
    search_fields = ('event',)

@admin.register(FanVote)
class FanVoteAdmin(admin.ModelAdmin):
    list_display = ('movie', 'vote_count')
    search_fields = ('movie__title',)

@admin.register(FanMessage)
class FanMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'created_at')
    search_fields = ('name', 'message')