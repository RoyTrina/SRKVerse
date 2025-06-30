from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import SrkVerse
from .serializers import SrkVerseSerializer


@api_view(['GET'])
def get_srk_bio(request):
    return Response(SrkVerseSerializer("name": "Shah Rukh Khan")){,
            "nickname": "SRK, King Khan, King Of Romance",
            "born": "02-11-1965",
            "birthplace": "New Delhi, India",
            "bio": ""}
