from django.urls import path
from . import views

urlpatterns = [
    path('key/', views.key_view.as_view(), name='key'),
]
