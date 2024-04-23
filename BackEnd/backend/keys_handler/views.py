from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import tools.mongobd as mongo
import tools.cipher as cipher
from bson import ObjectId
from .serializers import KeySerializer, InfoKeySerializer, AddKeySerializer, PutKeyUsernameSerializer, PutKeyPasswordSerializer, PutKeyDomainSerializer
from drf_yasg.utils import swagger_auto_schema

import logging

logger = logging.getLogger('your_app_logger')

# Create your views here.

class key_view(APIView):

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=AddKeySerializer)
    def post(self, request):

        try:
            data = request.data
            serializer = KeySerializer(data=data)

            bunchOfKeysId = data["bunchOfKeysId"]

            if serializer.is_valid():
                # Ouverture d'une connexion à la base de données MongoDB
                client = mongo.create_mongo_client()
                db = client["olok"]

                # Création d'une nouvelle clé
                key = serializer.data
                cipher_key = cipher.encrypt(key["password"])
                key["password"] = cipher_key[0]
                key["signature"] = cipher_key[1]
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

                    serializer.data.pop("password")

                    # loggage de la création de la clé
                    logger.info('new - ' + str(request.user.id) + ' - ' + str(id_document_key.inserted_id))

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class key_password_view(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, bunchOfKeysId, keyId):

        try:
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
                decipher_key = cipher.decrypt(key["password"], key["signature"])
                key["password"] = decipher_key[0]

                # Fermeture de la connexion à la base de données MongoDB
                client.close()

                # Vérification de la validité du mot de passe
                if key["signature"]:

                    # loggage de la récupération du mot de passe
                    logger.info('get - ' + str(request.user.id) + ' - ' + keyId)

                    return Response({"password": key.get("password")}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PutKeyPasswordSerializer)
    def put(self, request):

        try:
            data = request.data
            serializer = PutKeyPasswordSerializer(data=data)

            if serializer.is_valid():

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

                    # Chiffrement du nouveau mot de passe
                    cipher_key = cipher.encrypt(newPassword)

                    # Mise à jour du mot de passe
                    collection = db["keys"]
                    collection.update_one(
                        {"_id": ObjectId(keyId)},
                        {"$set": {"password": cipher_key[0]}}
                    )

                    # Mise à jour de la signature
                    collection.update_one(
                        {"_id": ObjectId(keyId)},
                        {"$set": {"signature": cipher_key[1]}
                    })

                    # Fermeture de la connexion à la base de données MongoDB
                    client.close()

                    # loggage de la mise à jour du mot de passe
                    logger.info('modif - ' + str(request.user.id) + ' - ' + keyId)

                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class key_username_view(APIView):

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=PutKeyUsernameSerializer)
    def put(self, request):

        try:
            data = request.data
            serializer = PutKeyUsernameSerializer(data=data)

            if serializer.is_valid():

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

                    # loggage de la mise à jour du nom d'utilisateur
                    logger.info('modif - ' + str(request.user.id) + ' - ' + keyId)

                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class key_domain_view(APIView):

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=PutKeyDomainSerializer)
    def put(self, request):

        try:
            data = request.data
            serializer = PutKeyDomainSerializer(data=data)

            if serializer.is_valid():
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

                    # loggage de la mise à jour du domaine
                    logger.info('modif - ' + str(request.user.id) + ' - ' + keyId)

                    return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class key_list_view(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, bunchOfKeysId):
        try:
            # Ouverture d'une connexion à la base de données MongoDB
            client = mongo.create_mongo_client()
            db = client["olok"]
            collection = db["bunchOfKeys"]

            # Récupérer le bunchOfKeys choisis par l'utilisateur
            bunchOfKeys = collection.find_one({"_id": ObjectId(bunchOfKeysId)})

            # On récupère la liste d'id des clés
            KeysIDs = bunchOfKeys.get("keysIDs", [])

            result = mongo.create_KeysList(db, KeysIDs)

            # Fermeture de la connexion à la base de données MongoDB
            client.close()

            return Response(result, status=status.HTTP_200_OK)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class key_delete_view(APIView):

    permission_classes = (IsAuthenticated,)

    def delete(self, request, bunchOfKeysId, keyId):

        try:
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

                # loggage de la suppression de la clé
                logger.info('del - ' + str(request.user.id) + ' - ' + keyId)

                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
