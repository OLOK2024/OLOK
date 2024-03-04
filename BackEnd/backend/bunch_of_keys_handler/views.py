import tools.jwt as jwt
import tools.mongobd as mongo
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BunchOfKeysSerializer, DelBunchOfKeysSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from bson import ObjectId

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
            bunchOfKeys  = mongo.create_bunchOfKeys(data["name"], data["description"], True, True, "normal")
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

    @swagger_auto_schema(request_body=DelBunchOfKeysSerializer)
    def delete(self, request):
        data = request.data
        serializer = DelBunchOfKeysSerializer(data=data)

        if serializer.is_valid():
            # Ouverture d'une connexion à la base de données MongoDB
            client = mongo.create_mongo_client()
            db = client["olok"]

            idUser = jwt.get_userId(request)

            collection = db["bunchOfKeys"]
            bunchOfKeys = collection.find_one({"_id": ObjectId(data["bunchOfKeysId"])})

            print(bunchOfKeys)

            # Vérification si on peut supprimer le porte trousseau
            if bunchOfKeys['deletable']:

                # Récupération de la liste des clés du porte trousseau
                listKeysIDs = bunchOfKeys.get("keysIDs", [])

                # Suppression de toute les clés du porte trousseau si contentDelete est à True
                # sinon transfert des clés dans le porte trousseau par défaut
                if data["contentDelete"]:
                    # Suppression de toute les clés du porte trousseau
                    collection = db["keys"]
                    collection.delete_many({"_id": {"$in": listKeysIDs}})
                else :
                    # Trouver le porte trousseau par défaut
                    collection = db["bunchOfKeysHolders"]
                    bunchOfKeysHolder = collection.find_one({"idOwner": idUser})
                    defaultBunchOfKeysId = bunchOfKeysHolder.get("bunchOfKeysIDs", [])[0]

                    # Ajout des clés dans le porte trousseau par défaut
                    collection = db["bunchOfKeys"]
                    collection.update_one(
                        {"_id": defaultBunchOfKeysId},
                        {"$push": {"keysIDs": {"$each": listKeysIDs}}
                    })

                # Suppression du porte trousseau
                collection = db["bunchOfKeys"]
                collection.delete_one({"_id": ObjectId(data["bunchOfKeysId"])})

                # Suppression du porte trousseau dans le porte trousseau holder
                collection = db["bunchOfKeysHolders"]
                collection.update_one(
                    {"idOwner": idUser},
                    {"$pull": {"bunchOfKeysIDs": ObjectId(data["bunchOfKeysId"])}
                })

                # Fermeture de la connexion à la base de données MongoDB
                client.close()

                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
