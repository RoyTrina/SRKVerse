"""
URL configuration for SRKVerse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Movies
    path('movies/', views.get_all_movies, name='movie-list'),
    path('movies/<int:year>/', views.get_movies_by_year_view, name='movies-by-year'),
    path('movie/<str:title>/', views.get_movie_by_title_view, name='movie-by-title'),
    path('movies/top-rated/', views.get_top_rated_view, name='top-rated'),
    path('movies/genres/<str:genre>/', views.get_by_genre_view, name='movies-by-genre'),

    # Songs
    path('songs/', views.get_all_songs, name='song-list'),
    path('movies/<str:title>/songs/', views.get_movie_songs, name='movie-songs'),
    path('songs/upload/', views.upload_song, name='upload-song'),

    # Quotes
    path('quotes/', views.get_all_quotes, name='quote-list'),
    path('quotes/random/', views.get_random_quote_view, name='random-quote'),
    path('quotes/movie/<str:title>/', views.get_quotes_by_movie_view, name='quotes-by-movie'),
    path('quotes/tag/<str:tag>/', views.get_quotes_by_tag_view, name='quotes-by-tag'),

    # Awards
    path('awards/', views.get_all_awards, name='award-list'),
    path('awards/<int:year>/', views.get_awards_by_year_view, name='awards-by-year'),
    path('awards/type/<str:award_type>/', views.get_awards_by_type_view, name='awards-by-type'),

    # Timeline
    path('timeline/', views.get_timeline_view, name='timeline'),
    path('events/<int:year>/', views.get_events_by_year_view, name='events-by-year'),
    path('debut/', views.get_debut_view, name='debut'),

    # Fan Interactions
    path('polls/favorite-movie/', views.get_votes_view, name='get-votes'),
    path('polls/favorite-movie/vote/', views.vote_favorite_view, name='vote-favorite'),
    path('fan-messages/', views.submit_message_view, name='submit-message'),

    # Quiz
    path('quiz/', views.get_quiz_view, name='quiz'),
    path('quiz/validate/', views.validate_quiz_view, name='validate-quiz'),
]