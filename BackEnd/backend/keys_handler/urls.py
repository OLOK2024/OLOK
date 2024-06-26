from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.key_view.as_view(), name='key'),
    re_path(r'^list(?:/(?P<bunchOfKeysId>\w+))/$', views.key_list_view.as_view(), name='key-list'),
    re_path(r'^password(?:/(?P<bunchOfKeysId>\w+)/(?P<keyId>\w+))?/$', views.key_password_view.as_view(), name='key-password'),
    re_path(r'^del(?:/(?P<bunchOfKeysId>\w+)/(?P<keyId>\w+))?/$', views.key_delete_view.as_view(), name='key-delete'),
    path('username/', views.key_username_view.as_view(), name='key-username'),
    path('domain/', views.key_domain_view.as_view(), name='key-domain'),
]
