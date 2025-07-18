from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Quote, Award, Timeline, FanVote, FanMessage, Song

class SRKVerseTests(TestCase):
    def setMovie(self):
        self.user = User.objects.create_user(username="fan123", password="testpass")
        self.movie = Movie.objects.create(
            tmdb_id=26022,
            title="My Name Is Khan",
            release_year=2010,
            description="An Indian Muslim with Asperger’s syndrome embarks on a journey.",
            role="Rizwan Khan",
            poster_path="/5Y36lmgVmbxJmN1jC8tiCkx6X1S.jpg",
            rating="7.9",
            genre=["Drama", "Romance"]
        )
    def test_movie_creation(self):
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(self.movie.title, "My Name Is Khan")


    def setQuote(self):
        self.user = User.objects.create_user(username="fan123", password="testpass")
        self.quote = Quote.objects.create(

        )
    def test_quote_creation(self):
            self.


    def setAward(self):
        self.