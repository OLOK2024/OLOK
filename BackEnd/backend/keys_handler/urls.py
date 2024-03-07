from django.urls import path, re_path
from . import views

urlpatterns = [
    path('key/', views.key_view.as_view(), name='key'),
    re_path(r'^key/password(?:/(?P<bunchOfKeysId>\w+)/(?P<keyId>\w+))?/$', views.key_password_view.as_view(), name='key-password'),
    path('key/username/', views.key_username_view.as_view(), name='key-username'),
    path('key/domain/', views.key_domain_view.as_view(), name='key-domain'),
]
