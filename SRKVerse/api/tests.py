from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Quote, Award, Timeline, FanVote, FanMessage, Song

class SRKVerseTests(TestCase):
    def setUp(self):
        # Create a test user and movie for all tests
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

    def test_quote_creation(self):
        quote = Quote.objects.create(
            text="My name is Khan, and I am not a terrorist.",
            movie=self.movie,
            context="Spoken by Rizwan Khan to assert his identity and challenge prejudice post-9/11.",
            tags=["inspirational", "identity"]
        )
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(quote.text, "My name is Khan, and I am not a terrorist.")

    def test_award_creation(self):
        award = Award.objects.create(
            title="Best Actor",
            year=2011,
            type="Filmfare",
            description="For outstanding performance as Rizwan Khan.",
            movie=self.movie
        )
        self.assertEqual(Award.objects.count(), 1)
        self.assertEqual(award.title, "Best Actor")

    def test_timeline_creation(self):
        timeline = Timeline.objects.create(
            year=1992,
            event="Debut in Deewana",
            description="Shah Rukh Khan debuted in Bollywood."
        )
        self.assertEqual(Timeline.objects.count(), 1)
        self.assertEqual(timeline.event, "Debut in Deewana")

    def test_favorite_creation(self):
        fan_vote = FanVote.objects.create(
            movie=self.movie,
            user=self.user,
            vote=150
        )
        self.assertEqual(FanVote.objects.count(), 1)
        self.assertEqual(fan_vote.vote_count, 150)

    def test_fan_message_creation(self):
        fan_message = FanMessage.objects.create(
            name="Amit Sharma",
            email="amit@example.com",
            message="SRK, you’re the king of Bollywood!"
        )
        self.assertEqual(FanMessage.objects.count(), 1)
        self.assertEqual(fan_message.name, "Amit Sharma")

    def test_song_creation(self):
        song = Song.objects.create(
            title="Tujh Mein Rab Dikhta Hai",
            movie=self.movie,
            composer="Salim-Sulaiman",
            lyricist="Jaideep Sahni",
            duration="4:43"
        )
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(song.title, "Tujh Mein Rab Dikhta Hai")