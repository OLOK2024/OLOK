from rest_framework import status
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from keys_handler.views import newKey_view
import tools.mongobd as mongo
import logging
import json
from bson import ObjectId

# Obtenez un logger pour votre application
logger = logging.getLogger('django')

class VerifyBunchOfKeysIdMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Vérifiez ici que le bunchOfKeysId appartient au token JWT
        # Si la vérification échoue, renvoyez une réponse 403 Forbidden
        # Si la vérification réussit, laissez la demande continuer normalement
        if request.method == 'POST' and view_func.view_class.__name__ in [newKey_view.__name__]:
            userId = get_userId(request)
            logger.info("userId: " + str(userId))
            data = json.loads(request.body)
            bunchOfKeysId = data.get('bunchOfKeysId')
            bunchOfKeysHolder = get_bunchOfKeysHolder(userId)
            print(bunchOfKeysHolder)

            if ObjectId(bunchOfKeysId) not in bunchOfKeysHolder.get('bunchOfKeysIDs', []):
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        return None

def get_userId(request):
    jwt_authentication = JWTAuthentication()
    user, _ = jwt_authentication.authenticate(request)
    return user.id

def get_bunchOfKeysHolder(bunchOfKeysHolderOwnerId):
    client = mongo.create_mongo_client()
    db = client["olok"]
    collection = db["bunchOfKeysHolders"]

    # Recherche du bunchOfKeysHolder
    bunchOfKeysHolder = collection.find_one({"idOwner": bunchOfKeysHolderOwnerId})

    client.close()
    return bunchOfKeysHolder