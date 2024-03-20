from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
import tools.mongobd as mongo
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger('your_app_logger')

class signup_view(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        # Récupération des données de l'utilisateur
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            # Enregistrement de l'utilisateur dans la base de données
            serializer.save()

            # Création d'une nouvelle connexion à la base de données MongoDB
            client = mongo.create_mongo_client()
            db = client["olok"]

            # Création de son porte trousseau par défaut
            bunchOfKeysHolder = mongo.create_bunchOfKeysHolder(serializer.data["id"])
            collection = db["bunchOfKeysHolders"]
            id_document_bunchOfKeysHolder = collection.insert_one(bunchOfKeysHolder)

            # Création d'un porte trousseau par défaut
            bunchOfKeysDefault = mongo.create_bunchOfKeys("default bunch of keys", "this is the default bunch of keys", False, False, "default")
            bunchOfKeysFavorite = mongo.create_bunchOfKeys("favorite bunch of keys", "this is the favorite bunch of keys", False, False, "favorite")
            collection = db["bunchOfKeys"]
            id_document_bunchOfKeysDefault = collection.insert_one(bunchOfKeysDefault)
            id_document_bunchOfKeysFavorite = collection.insert_one(bunchOfKeysFavorite)

            # Ajout du trousseau par défaut dans le porte trousseau par défaut
            collection = db["bunchOfKeysHolders"]
            collection.update_one(
                {"_id": id_document_bunchOfKeysHolder.inserted_id},
                {"$push": {"bunchOfKeysIDs": id_document_bunchOfKeysDefault.inserted_id}}
            )
            collection.update_one(
                {"_id": id_document_bunchOfKeysHolder.inserted_id},
                {"$push": {"bunchOfKeysIDs": id_document_bunchOfKeysFavorite.inserted_id}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            # loggage de la création du compte
            logger.info('creation of an account ' + str(serializer.data["id"]))

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
