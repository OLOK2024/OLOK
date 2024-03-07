from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PutProfileDataSerializer
from authentification.models import User
from drf_yasg.utils import swagger_auto_schema

import tools.jwt as jwt

# Create your views here.

class profile_view(APIView):

    @swagger_auto_schema(request_body=PutProfileDataSerializer)
    def put(self, request):
        data = request.data
        serializer = PutProfileDataSerializer(data=data)

        if serializer.is_valid():

            user = User.objects.get(id=jwt.get_userId(request))

            # Mise à jour des données
            user.first_name = serializer.data["first_name"]
            user.last_name = serializer.data["last_name"]
            user.end_of_day = serializer.data["end_of_day"]
            user.start_of_day = serializer.data["start_of_day"]
            user.workdays = serializer.data["workdays"]
            user.country_code = serializer.data["country_code"]

            # Sauvegarde des données
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass