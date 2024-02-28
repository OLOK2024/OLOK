from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


@api_view(['POST'])
@csrf_exempt
def signup_view(request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

