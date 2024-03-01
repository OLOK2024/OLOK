from django.urls import path
from . import views

urlpatterns = [
    path('newKey/', views.newKey_view.as_view(), name='newKey'),
]
