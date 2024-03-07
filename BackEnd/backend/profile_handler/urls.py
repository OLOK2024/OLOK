from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view.as_view(), name='profile'),
]
