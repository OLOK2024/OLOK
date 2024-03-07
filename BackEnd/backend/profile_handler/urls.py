from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view.as_view(), name='profile'),
    path('change_password/', views.change_password_view.as_view(), name='change_password'),
]
