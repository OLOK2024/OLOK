from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in


@api_view(['POST'])
@csrf_exempt
def signup_view(request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email, password=password)
        if user:
            try:
                token = RefreshToken.for_user(user)
                token["email"] = user.email
                access_token = str(token.access_token)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = access_token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)

"""
@api_view(['POST'])
@csrf_exempt
def logout_view(request):
    try:
        refresh_token = request.COOKIES["refresh_token"]
        RefreshToken(refresh_token).blacklist()
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)
"""
