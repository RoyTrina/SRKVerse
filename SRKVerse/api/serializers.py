from rest_framework import serializers
from .models import SRKVerse


class SRKVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRKVerse
        fields = '__all__'
