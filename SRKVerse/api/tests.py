import os
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Movie, Song, Quote, Award, Timeline, FanVote, FanMessage
from .serializers import SongUploadSerializer
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
import spotipy.exceptions

class SRKVerseModelTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            tmdb_id=12345,
            title="Dilwale Dulhania Le Jayenge",
            release_year=1995,
            description="A romantic drama",
            role="Raj Malhotra",
            poster_path="/path/to/poster.jpg",
            rating=8.0,
            genres=["Romance", "Drama"]
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Dilwale Dulhania Le Jayenge")

    def test_song_str(self):
        song = Song.objects.create(
            title="Tujhe Dekha To",
            movie=self.movie,
            composer="Jatin-Lalit",
            lyricist="Anand Bakshi",
            duration=300
        )
        self.assertEqual(str(song), "Tujhe Dekha To - Dilwale Dulhania Le Jayenge")

    def test_quote_str(self):
        quote = Quote.objects.create(
            text="Picture abhi baaki hai mere dost.",
            movie=self.movie,
            context="From Om Shanti Om",
            tags=["iconic"]
        )
        self.assertEqual(str(quote), "Picture abhi baaki hai mere dost.")

    def test_award_str(self):
        award = Award.objects.create(
            title="Filmfare Best Actor",
            year=1993,
            type="Filmfare",
            description="For Baazigar",
            movie=self.movie
        )
        self.assertEqual(str(award), "Filmfare Best Actor (1993)")

    def test_timeline_str(self):
        timeline = Timeline.objects.create(
            year=1992,
            event="Debut in Deewana",
            description="Shah Rukh Khan's first film"
        )
        self.assertEqual(str(timeline), "Debut in Deewana (1992)")

    def test_fan_vote_str(self):
        vote = FanVote.objects.create(movie=self.movie, vote_count=100)
        self.assertEqual(str(vote), "Dilwale Dulhania Le Jayenge: 100 votes")

    def test_fan_message_str(self):
        message = FanMessage.objects.create(name="Fan", message="Love SRK!")
        self.assertEqual(str(message), "Fan: Love SRK!")

class SpotifyIntegrationTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            tmdb_id=12345, title="Dilwale Dulhania Le Jayenge", release_year=1995
        )
        self.song = Song.objects.create(
            title="Tujhe Dekha To", movie=self.movie, composer="Jatin-Lalit"
        )

    @patch('api.services.get_spotify_client')
    def test_enhance_song_with_spotify_mocked(self, mock_client):
        mock_sp = MagicMock()
        mock_track = {
            'id': 'mock_spotify_id',
            'preview_url': 'https://p.scdn.co/mp3-preview/mock.mp3',
            'popularity': 85,
            'duration_ms': 300000
        }
        mock_sp.search.return_value = {
            'tracks': {'items': [mock_track]}
        }
        mock_client.return_value = mock_sp

        from .services import enhance_song_with_spotify
        enhance_song_with_spotify("Tujhe Dekha To", "Dilwale Dulhania Le Jayenge")

        updated_song = Song.objects.get(id=self.song.id)
        self.assertEqual(updated_song.spotify_id, 'mock_spotify_id')
        self.assertEqual(updated_song.preview_url, 'https://p.scdn.co/mp3-preview/mock.mp3')
        self.assertEqual(updated_song.popularity, 85)
        self.assertEqual(updated_song.duration, 300)

    @patch('api.services.get_spotify_client')
    def test_enhance_song_spotify_rate_limit(self, mock_client):
        mock_sp = MagicMock()
        mock_sp.search.side_effect = spotipy.exceptions.SpotifyException(
            429, message="API rate limit exceeded"
        )
        mock_client.return_value = mock_sp

        from .services import enhance_song_with_spotify
        with self.assertRaises(ValidationError) as cm:
            enhance_song_with_spotify("Tujhe Dekha To", "Dilwale Dulhania Le Jayenge")
        self.assertEqual(str(cm.exception), "Spotify rate limit exceeded. Please try again later.")

    @patch('api.services.get_spotify_client')
    def test_enhance_song_spotify_auth_failure(self, mock_client):
        mock_client.side_effect = ValidationError("Spotify authentication failed: Invalid credentials")
        from .services import enhance_song_with_spotify
        with self.assertRaises(ValidationError) as cm:
            enhance_song_with_spotify("Tujhe Dekha To", "Dilwale Dulhania Le Jayenge")
        self.assertIn("Spotify authentication failed", str(cm.exception))

    @patch.dict('django.conf.settings', {
        'SPOTIFY_CLIENT_ID': 'test_id',
        'SPOTIFY_CLIENT_SECRET': 'test_secret'
    })
    def test_enhance_song_with_spotify_real(self):
        import os
        if os.getenv('RUN_SPOTIFY_LIVE_TESTS', 'false') == 'true':
            from .services import enhance_song_with_spotify
            try:
                enhance_song_with_spotify("Tujhe Dekha To", "Dilwale Dulhania Le Jayenge")
                updated_song = Song.objects.get(id=self.song.id)
                self.assertIsNotNone(updated_song.spotify_id)
            except ValidationError as e:
                self.fail(f"Live Spotify test failed: {str(e)}")
        else:
            self.skipTest("Skipping live Spotify test; set RUN_SPOTIFY_LIVE_TESTS=true")

class SRKVerseAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            tmdb_id=12345,
            title="Dilwale Dulhania Le Jayenge",
            release_year=1995,
            description="A romantic drama",
            role="Raj Malhotra",
            poster_path="/path/to/poster.jpg",
            rating=8.0,
            genres=["Romance", "Drama"]
        )
        self.song = Song.objects.create(
            title="Tujhe Dekha To",
            movie=self.movie,
            composer="Jatin-Lalit",
            lyricist="Anand Bakshi",
            duration=300
        )
        self.quote = Quote.objects.create(
            text="Picture abhi baaki hai mere dost.",
            movie=self.movie,
            context="From Om Shanti Om",
            tags=["iconic"]
        )
        self.award = Award.objects.create(
            title="Filmfare Best Actor",
            year=1993,
            type="Filmfare",
            description="For Baazigar",
            movie=self.movie
        )
        self.timeline = Timeline.objects.create(
            year=1992,
            event="Debut in Deewana",
            description="Shah Rukh Khan's first film"
        )
        self.fan_vote = FanVote.objects.create(movie=self.movie, vote_count=100)
        self.fan_message = FanMessage.objects.create(name="Fan", message="Love SRK!")

    def test_get_all_movies(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Dilwale Dulhania Le Jayenge")

    def test_get_movies_by_year(self):
        response = self.client.get(reverse('movies-by-year', args=[1995]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movie_by_title(self):
        response = self.client.get(reverse('movie-by-title', args=['Dilwale Dulhania Le Jayenge']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Dilwale Dulhania Le Jayenge")

    def test_get_movie_by_title_not_found(self):
        response = self.client.get(reverse('movie-by-title', args=['Nonexistent Movie']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Movie not found")

    def test_get_all_songs(self):
        response = self.client.get(reverse('song-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Tujhe Dekha To")

    def test_get_movie_songs(self):
        response = self.client.get(reverse('movie-songs', args=['Dilwale Dulhania Le Jayenge']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Tujhe Dekha To")

    def test_get_movie_songs_not_found(self):
        response = self.client.get(reverse('movie-songs', args=['Nonexistent Movie']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Movie not found")

    def test_upload_song_valid(self):
        with open('test_song.mp3', 'wb') as f:
            f.write(b"Fake MP3 content")
        upload_file = SimpleUploadedFile('test_song.mp3', b"Fake MP3 content", content_type='audio/mpeg')
        data = {
            'title': 'Yeh Dil Deewana',
            'movie_title': 'Dilwale Dulhania Le Jayenge',
            'composer': 'Jatin-Lalit',
            'lyricist': 'Anand Bakshi',
            'audio_file': upload_file
        }
        with patch('api.views.enhance_song_with_spotify') as mock_enhance:
            response = self.client.post(reverse('upload-song'), data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['message'], 'Song uploaded successfully')
            self.assertEqual(Song.objects.count(), 2)
            mock_enhance.assert_called_once_with('Yeh Dil Deewana', 'Dilwale Dulhania Le Jayenge')
        os.remove('test_song.mp3')

    def test_upload_song_duplicate(self):
        with open('test_song.mp3', 'wb') as f:
            f.write(b"Fake MP3 content")
        upload_file = SimpleUploadedFile('test_song.mp3', b"Fake MP3 content", content_type='audio/mpeg')
        data = {
            'title': 'Tujhe Dekha To',
            'movie_title': 'Dilwale Dulhania Le Jayenge',
            'audio_file': upload_file
        }
        response = self.client.post(reverse('upload-song'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Song or album already available', str(response.data['error']))
        os.remove('test_song.mp3')

    def test_upload_song_invalid_file_type(self):
        with open('test.txt', 'wb') as f:
            f.write(b"Invalid content")
        upload_file = SimpleUploadedFile('test.txt', b"Invalid content", content_type='text/plain')
        data = {
            'title': 'Yeh Dil Deewana',
            'movie_title': 'Dilwale Dulhania Le Jayenge',
            'audio_file': upload_file
        }
        response = self.client.post(reverse('upload-song'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid file format', str(response.data['error']))
        os.remove('test.txt')

    def test_upload_song_too_large(self):
        with open('test_song.mp3', 'wb') as f:
            f.write(b"A" * (6 * 1024 * 1024))  # 6MB
        upload_file = SimpleUploadedFile('test_song.mp3', b"A" * (6 * 1024 * 1024), content_type='audio/mpeg')
        data = {
            'title': 'Yeh Dil Deewana',
            'movie_title': 'Dilwale Dulhania Le Jayenge',
            'audio_file': upload_file
        }
        response = self.client.post(reverse('upload-song'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('File size exceeds 5MB limit', str(response.data['error']))
        os.remove('test_song.mp3')

    def test_upload_song_spotify_failure(self):
        with open('test_song.mp3', 'wb') as f:
            f.write(b"Fake MP3 content")
        upload_file = SimpleUploadedFile('test_song.mp3', b"Fake MP3 content", content_type='audio/mpeg')
        data = {
            'title': 'Yeh Dil Deewana',
            'movie_title': 'Dilwale Dulhania Le Jayenge',
            'audio_file': upload_file
        }
        with patch('api.views.enhance_song_with_spotify', side_effect=ValidationError("Spotify rate limit exceeded")):
            response = self.client.post(reverse('upload-song'), data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('Spotify metadata could not be fetched', response.data['message'])
            self.assertEqual(Song.objects.count(), 2)
        os.remove('test_song.mp3')

    def test_get_all_quotes(self):
        response = self.client.get(reverse('quote-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_random_quote(self):
        with patch('api.views.get_random_quote', return_value=self.quote):
            response = self.client.get(reverse('random-quote'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['text'], "Picture abhi baaki hai mere dost.")

    def test_get_quotes_by_movie(self):
        response = self.client.get(reverse('quotes-by-movie', args=['Dilwale Dulhania Le Jayenge']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_quotes_by_tag(self):
        response = self.client.get(reverse('quotes-by-tag', args=['iconic']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_all_awards(self):
        response = self.client.get(reverse('award-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_awards_by_year(self):
        response = self.client.get(reverse('awards-by-year', args=[1993]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_awards_by_type(self):
        response = self.client.get(reverse('awards-by-type', args=['Filmfare']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_timeline(self):
        response = self.client.get(reverse('timeline'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_events_by_year(self):
        response = self.client.get(reverse('events-by-year', args=[1992]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_debut(self):
        with patch('api.views.get_debut', return_value=self.timeline):
            response = self.client.get(reverse('debut'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['event'], "Debut in Deewana")

    def test_get_votes(self):
        response = self.client.get(reverse('get-votes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vote_favorite(self):
        data = {'title': 'Dilwale Dulhania Le Jayenge'}
        with patch('api.views.vote_favorite', return_value=self.fan_vote):
            response = self.client.post(reverse('vote-favorite'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_submit_fan_message(self):
        data = {'name': 'Fan2', 'message': 'SRK is the best!'}
        response = self.client.post(reverse('submit-message'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Thank you Fan2 for your message!', response.data['message'])

    def test_get_quiz(self):
        with patch('api.views.get_quiz', return_value={
            'question': 'Which movie?',
            'options': ['A', 'B', 'C', 'D'],
            'answer': 'A'
        }):
            response = self.client.get(reverse('quiz'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['question'], 'Which movie?')

    def test_validate_quiz(self):
        data = {'title': 'Dilwale Dulhania Le Jayenge', 'answer': 'Some quote'}
        with patch('api.views.validate_quiz', return_value={'correct': True, 'message': 'Correct!'}) as mock_validate:
            response = self.client.post(reverse('validate-quiz'), data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['correct'])
            mock_validate.assert_called_once_with('Dilwale Dulhania Le Jayenge', 'Some quote')