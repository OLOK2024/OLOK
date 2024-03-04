import tools.jwt as jwt
import tools.mongobd as mongo
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BunchOfKeysSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class bunchOfKey_view(APIView):

    @swagger_auto_schema(request_body=BunchOfKeysSerializer)
    def post(self, request):
        data = request.data
        serializer = BunchOfKeysSerializer(data=data)

        if serializer.is_valid():
            # Ouverture d'une connexion à la base de données MongoDB
            client = mongo.create_mongo_client()
            db = client["olok"]

            idUser = jwt.get_userId(request)

            # Création d'un nouveau porte trousseau
            bunchOfKeys  = mongo.create_bunchOfKeys(data["name"], data["description"], True, "normal")
            collection = db["bunchOfKeys"]

            # Enregistrement du porte trousseau
            id_document_bunchOfKeys = collection.insert_one(bunchOfKeys)

            # Vérification de la création du porte trousseau
            if id_document_bunchOfKeys.inserted_id:
                # Ajout du porte trousseau dans le porte trousseau holder
                collection = db["bunchOfKeysHolders"]
                collection.update_one(
                    {"idOwner": idUser},
                    {"$push": {"bunchOfKeysIDs": id_document_bunchOfKeys.inserted_id}}
                )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
