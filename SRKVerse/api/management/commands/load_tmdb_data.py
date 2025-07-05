from django.core.management.base import BaseCommand

from SRKVerse.api.services import load_movies, load_awards, load_timeline, load_quotes


class Command(BaseCommand):
    help = 'Load Shah Rukh Khan movies, quotes, awards, and timeline into the database'

    def handle(self, *args, **options):
        movies = load_movies()
        load_timeline()
        load_awards()
        load_quotes()
        self.stdout.write(self.style.SUCCESS(f'Loaded {movies.count()} movies, quotes, awards, and timeline.'))
