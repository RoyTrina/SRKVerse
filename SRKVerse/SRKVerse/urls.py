from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SRKVerse.api.views import (
    get_all_movies,
    get_movies_by_year_view,
    get_movie_by_title_view,
    get_top_rated_view,
    get_by_genre_view,
    get_all_quotes,
    get_random_quote_view,
    get_quotes_by_movie_view,
    get_quotes_by_tag_view,
    get_all_awards,
    get_awards_by_year_view,
    get_awards_by_type_view,
    get_timeline_view,
    get_events_by_year_view,
    get_debut_view,
    get_votes_view,
    vote_favorite_view,
    get_quiz_view,
    validate_quiz_view,
    submit_message_view
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('SRKVerse.urls')),  # Include the api app's URLs

                  # Movie Endpoints
                  path('srk/movies/', get_all_movies, name='movie-list'),
                  path('srk/movies/<int:year>/', get_movies_by_year_view, name='movies-by-year'),
                  path('srk/movie/<str:title>/', get_movie_by_title_view, name='movie-by-title'),
                  path('srk/movies/top-rated/', get_top_rated_view, name='top-rated-movies'),
                  path('srk/movies/genres/<str:genre>/', get_by_genre_view, name='movies-by-genre'),

                  # Quote Endpoints
                  path('srk/quotes/', get_all_quotes, name='quote-list'),
                  path('srk/quotes/random/', get_random_quote_view, name='random-quote'),
                  path('srk/quotes/movie/<str:title>/', get_quotes_by_movie_view, name='quotes-by-movie'),
                  path('srk/quotes/tag/<str:tag>/', get_quotes_by_tag_view, name='quotes-by-tag'),

                  # Award Endpoints
                  path('srk/awards/', get_all_awards, name='award-list'),
                  path('srk/awards/<int:year>/', get_awards_by_year_view, name='awards-by-year'),
                  path('srk/awards/type/<str:award_type>/', get_awards_by_type_view, name='awards-by-type'),

                  # Timeline Endpoints
                  path('srk/timeline/', get_timeline_view, name='timeline'),
                  path('srk/events/<int:year>/', get_events_by_year_view, name='events-by-year'),
                  path('srk/debut/', get_debut_view, name='debut'),

                  # Fan Interaction Endpoints
                  path('srk/polls/favorite-movie/', get_votes_view, name='get-votes'),
                  path('srk/polls/favorite-movie/vote/', vote_favorite_view, name='vote-favorite'),
                  path('srk/quiz/', get_quiz_view, name='quiz'),
                  path('srk/quiz/validate/', validate_quiz_view, name='validate-quiz'),
                  path('srk/fan-messages/', submit_message_view, name='submit-message'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
