from rest_framework import status
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from keys_handler.views import key_view
from bunch_of_keys_handler.views import bunchOfKey_view, keyBunchOfKeys_view
import tools.mongobd as mongo
import tools.jwt as jwt
import logging
import json
from bson import ObjectId

# Obtenez un logger pour votre application
logger = logging.getLogger('django')

class VerifyLegitOwnerMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Vérifiez ici que le bunchOfKeysId appartient au token JWT
        # Si la vérification échoue, renvoyez une réponse 403 Forbidden
        # Si la vérification réussit, laissez la demande continuer normalement
        if request.method in ['POST', 'DELETE', 'PUT'] and view_func.view_class.__name__ in [key_view.__name__]:
            data = json.loads(request.body)
            bunchOfKeysId = data.get('bunchOfKeysId')
            if not isLegitOwner(request, bunchOfKeysId):
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        if request.method in ['GET'] and view_func.view_class.__name__ in [key_view.__name__]:
            bunchOfKeysId = request.resolver_match.kwargs.get('bunchOfKeysId')
            if not isLegitOwner(request, bunchOfKeysId):
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        if request.method in ['DELETE', 'PUT'] and view_func.view_class.__name__ in [bunchOfKey_view.__name__]:
            data = json.loads(request.body)
            bunchOfKeysId = data.get('bunchOfKeysId')
            if not isLegitOwner(request, bunchOfKeysId):
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        if request.method in ['PUT'] and view_func.view_class.__name__ in [keyBunchOfKeys_view.__name__]:
            data = json.loads(request.body)
            bunchOfKeysId = data.get('bunchOfKeysId')
            newBunchOfKeysId = data.get('newBunchOfKeysId')
            if not isLegitOwner(request, bunchOfKeysId) or not isLegitOwner(request, newBunchOfKeysId):
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return None

def get_bunchOfKeysHolderByOwnerId(bunchOfKeysHolderOwnerId):
    client = mongo.create_mongo_client()
    db = client["olok"]
    collection = db["bunchOfKeysHolders"]

    # Recherche du bunchOfKeysHolder
    bunchOfKeysHolder = collection.find_one({"idOwner": bunchOfKeysHolderOwnerId})

    client.close()
    return bunchOfKeysHolder

def isLegitOwner(request, bunchOfKeysId):
    userId = jwt.get_userId(request)
    bunchOfKeysHolder = get_bunchOfKeysHolderByOwnerId(userId)
    return ObjectId(bunchOfKeysId) in bunchOfKeysHolder.get('bunchOfKeysIDs', [])