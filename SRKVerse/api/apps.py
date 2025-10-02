from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Song
import mimetypes
import mutagen
from django.core.exceptions import ValidationError

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'SRKVerse API'

    def ready(self):
        # Connect signal for song uploads
        @receiver(post_save, sender=Song)
        def validate_song_upload(sender, instance, created, **kwargs):
            if created and instance.audio_file:
                # Validate file type
                mime_type, _ = mimetypes.guess_type(instance.audio_file.path)
                if mime_type not in ['audio/mpeg', 'audio/mp3', 'audio/wav']:
                    instance.delete()  # Remove invalid file
                    raise ValidationError("Invalid audio file format. Only MP3 or WAV allowed.")

                # Extract duration using mutagen
                try:
                    audio = mutagen.File(instance.audio_file.path)
                    instance.duration = int(audio.info.length) if audio else instance.duration
                    instance.save()
                except Exception as e:
                    print(f"Failed to extract duration: {e}")