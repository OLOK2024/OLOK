from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.key_view.as_view(), name='key'),
    re_path(r'^password(?:/(?P<bunchOfKeysId>\w+)/(?P<keyId>\w+))?/$', views.key_password_view.as_view(), name='key-password'),
    path('username/', views.key_username_view.as_view(), name='key-username'),
    path('domain/', views.key_domain_view.as_view(), name='key-domain'),
]
