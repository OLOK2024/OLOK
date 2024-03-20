from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import PutProfileDataSerializer, ChangePasswordSerializer
from authentification.models import User
from drf_yasg.utils import swagger_auto_schema

import tools.jwt as jwt
import tools.mongobd as mongo
import logging

logger = logging.getLogger('your_app_logger')

# Create your views here.

class profile_view(APIView):

    permission_classes = (IsAuthenticated,)

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

            # loggage de la mise à jour du profil
            logger.info('update profile ' + str(user.id))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        userId = jwt.get_userId(request)

        # On se connecte à la base de données mongo
        client = mongo.create_mongo_client()
        db = client["olok"]

        # On récupère le porte trousseau holder
        collection = db["bunchOfKeysHolders"]
        bunchOfKeysHolder = collection.find_one({"idOwner": userId})

        # On supprime chaque trousseau
        for bunchOfKeysId in bunchOfKeysHolder["bunchOfKeysIDs"]:
            collection = db["bunchOfKeys"]
            bunchOfKeys = collection.find_one({"_id": bunchOfKeysId})

            # On supprime les clés du trousseau
            collection = db["keys"]
            for keyId in bunchOfKeys["keysIDs"]:
                collection.delete_one({"_id": keyId})

            # On supprime le trousseau
            collection = db["bunchOfKeys"]
            collection.delete_one({"_id": bunchOfKeysId})

        # On supprime le porte trousseau holder
        collection = db["bunchOfKeysHolders"]
        collection.delete_one({"idOwner": userId})

        # On se déconnecte de la base de données mongo
        client.close()

        # On supprime l'utilisateur
        user = User.objects.get(id=userId)
        user.delete()

        # loggage de la suppression du compte
        logger.info('delete account ' + str(userId))

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        userId = jwt.get_userId(request)
        user = User.objects.get(id=userId)
        serializer = PutProfileDataSerializer(user)

        # loggage de la récupération du profil
        logger.info('get profile ' + str(userId))

        return Response(serializer.data, status=status.HTTP_200_OK)

class change_password_view(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):

        # Loggage de la mise à jour du mot de passe
        logger.info('update password ' + str(self.request.user.id))

        # Get the user object based on the JWT payload
        return self.request.user