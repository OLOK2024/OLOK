from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import tools.mongobd as mongo
from bson import ObjectId
from .serializers import KeySerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class newKey_view(APIView):
    @swagger_auto_schema(request_body=KeySerializer)
    def post(self, request):
        data = request.data
        serializer = KeySerializer(data=data)

        bunchOfKeysId = data["bunchOfKeysId"]

        if serializer.is_valid():
            # Ouverture d'une connexion à la base de données MongoDB
            client = mongo.create_mongo_client()
            db = client["olok"]

            # Création d'une nouvelle clé
            key = serializer.data
            collection = db["keys"]
            id_document_key = collection.insert_one(key)

            # Vérification de la création de la clé
            if id_document_key.inserted_id:
                # Ajout de la clé dans le porte trousseau
                collection = db["bunchOfKeys"]
                collection.update_one(
                    {"_id": ObjectId(bunchOfKeysId)},
                    {"$push": {"keysIDs": id_document_key.inserted_id}}
                )

                # Fermeture de la connexion à la base de données MongoDB
                client.close()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    