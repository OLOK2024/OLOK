from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import tools.mongobd as mongo
from bson import ObjectId
from .serializers import KeySerializer
from .dto_serializers import AddKeySerializer, InfoKeySerializer, PutKeyUsernameSerializer, PutKeyPasswordSerializer, PutKeyDomainSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class key_view(APIView):

    @swagger_auto_schema(request_body=AddKeySerializer)
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

    @swagger_auto_schema(request_body=InfoKeySerializer)
    def delete(self, request):
        data = request.data
        keyId = data["keyId"]
        bunchOfKeysId = data["bunchOfKeysId"]

        # Ouverture d'une connexion à la base de données MongoDB
        client = mongo.create_mongo_client()
        db = client["olok"]

        # Vérification de l'existence de la clé
        collection = db["bunchOfKeys"]
        bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

        if ObjectId(keyId) in bunchOfKeys.get("keysIDs", []):
            # Suppression de la clé
            collection = db["keys"]
            collection.delete_one({"_id": ObjectId(keyId)})

            # Suppression de la clé dans le porte trousseau
            collection = db["bunchOfKeys"]
            collection.update_one(
                {"_id": ObjectId(bunchOfKeysId)},
                {"$pull": {"keysIDs": ObjectId(keyId)}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class key_password_view(APIView):

    #@swagger_auto_schema(request_body=InfoKeySerializer)
    def get(self, request, bunchOfKeysId, keyId):

        # Ouverture d'une connexion à la base de données MongoDB
        client = mongo.create_mongo_client()
        db = client["olok"]

        # Vérification de l'existence de la clé
        collection = db["bunchOfKeys"]
        bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

        if ObjectId(keyId) in bunchOfKeys.get("keysIDs", []):
            # Récupération du mot de passe
            collection = db["keys"]
            key = collection.find_one({"_id": ObjectId(keyId)})

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response({"password": key.get("password")}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PutKeyPasswordSerializer)
    def put(self, request):
        data = request.data
        bunchOfKeysId = data["bunchOfKeysId"]
        keyId = data["keyId"]
        newPassword = data["newPassword"]

        # Ouverture d'une connexion à la base de données MongoDB
        client = mongo.create_mongo_client()
        db = client["olok"]

        # Vérification de l'existence de la clé
        collection = db["bunchOfKeys"]
        bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

        if ObjectId(keyId) in bunchOfKeys.get("keysIDs", []):
            # Mise à jour du mot de passe
            collection = db["keys"]
            collection.update_one(
                {"_id": ObjectId(keyId)},
                {"$set": {"password": newPassword}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class key_username_view(APIView):

    @swagger_auto_schema(request_body=PutKeyUsernameSerializer)
    def put(self, request):
        data = request.data
        bunchOfKeysId = data["bunchOfKeysId"]
        keyId = data["keyId"]
        newUsername = data["newUsername"]

        # Ouverture d'une connexion à la base de données MongoDB
        client = mongo.create_mongo_client()
        db = client["olok"]

        # Vérification de l'existence de la clé
        collection = db["bunchOfKeys"]
        bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

        if ObjectId(keyId) in bunchOfKeys.get("keysIDs", []):
            # Mise à jour du nom d'utilisateur
            collection = db["keys"]
            collection.update_one(
                {"_id": ObjectId(keyId)},
                {"$set": {"username": newUsername}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class key_domain_view(APIView):

    @swagger_auto_schema(request_body=PutKeyDomainSerializer)
    def put(self, request):
        data = request.data
        bunchOfKeysId = data["bunchOfKeysId"]
        keyId = data["keyId"]
        newDomain = data["newDomain"]

        # Ouverture d'une connexion à la base de données MongoDB
        client = mongo.create_mongo_client()
        db = client["olok"]

        # Vérification de l'existence de la clé
        collection = db["bunchOfKeys"]
        bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

        if ObjectId(keyId) in bunchOfKeys.get("keysIDs", []):
            # Mise à jour du domaine
            collection = db["keys"]
            collection.update_one(
                {"_id": ObjectId(keyId)},
                {"$set": {"domain": newDomain}}
            )

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)