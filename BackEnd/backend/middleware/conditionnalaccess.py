import requests
from rest_framework import status
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentification.models import User

import tools.jwt as jwt
import json

class VerifyVpnIdMiddleware(MiddlewareMixin):
	def process_view(self, request, view_func, view_args, view_kwargs):
		# Si la vérification détecte le vpn alors connexion bloqué
		# Si la vérification ne détecte pas le vpn alors laissez la demande continuer normalement
		if request.method == 'POST' and view_func.view_class.__name__ in [ TokenObtainPairView.__name__]:

			data = json.loads(request.body)
			user = User.objects.get(email=data.get('email'))
			print(user.country_code)				
			if detect_vpn(request)[0] or detect_vpn(request)[1] != user.country_code :
				return HttpResponse(status=status.HTTP_403_FORBIDDEN)

		if request.method == 'POST' and view_func.view_class.__name__ in [ TokenRefreshView.__name__]:

			user = User.objects.get(id=jwt.get_userId(request))

			if detect_vpn(request)[0] or detect_vpn(request)[1] !=  user.country_code :
				return HttpResponse(status=status.HTTP_403_FORBIDDEN)
		return None
	
def index(request):
	visitor_ip = request.META.get('REMOTE_ADDR')
	return {visitor_ip}

def detect_vpn(request):
	ip = index(request)
	#Pour les tests en local
	#ip = "173.179.157.67"
	try:
		response = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy,countryCode")
		data = response.json()
		print(data)
		return (data["proxy"],data["countryCode"])
	except Exception as e:
		print("Unable to detect VPN:", e)
		return (False,"CA")