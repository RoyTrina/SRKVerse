from django.core.management.base import BaseCommand

from SRKVerse.api.services import load_movies, load_awards, load_timeline, load_quotes


class Command(BaseCommand):
    help = 'Load Shah Rukh Khan movies, quotes, awards, and timeline into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading movies from TMDB...')
        load_movies()
        self.stdout.write('Successfully loaded movies from TMDB.')

        self.stdout.write('Loading timeline...')
        load_timeline()
        self.stdout.write('Successfully loaded timeline.')

        self.stdout.write('Loading awards...')
        load_awards()
        self.stdout.write('Successfully loaded awards.')

        self.stdout.write('Loading quotes...')
        load_quotes()
        self.stdout.write('Successfully loaded quotes.')
