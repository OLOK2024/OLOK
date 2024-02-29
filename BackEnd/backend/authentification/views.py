from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
import tools.mongobd as mongo

class signup_view(APIView):
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
            bunchOfKeysHolder = mongo.create_bunchOfKeysHolder(serializer.data["id"], "normal")
            collection = db["bunchOfKeysHolders"]
            id_document_bunchOfKeysHolder = collection.insert_one(bunchOfKeysHolder)

            # Création d'un porte trousseau par défaut
            bunchOfKeys = mongo.create_bunchOfKeys("default bunch of keys", "this is the default bunch of keys", False)
            collection = db["bunchOfKeys"]
            id_document_bunchOfKeys = collection.insert_one(bunchOfKeys)

            # Ajout du trousseau par défaut dans le porte trousseau par défaut
            collection = db["bunchOfKeysHolders"]
            collection.update_one(
                {"_id": id_document_bunchOfKeysHolder.inserted_id},
                {"$push": {"bunchOfKeysIDs": id_document_bunchOfKeys.inserted_id}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
