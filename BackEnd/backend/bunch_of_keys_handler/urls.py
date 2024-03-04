from django.urls import path
from . import views

urlpatterns = [
    path('', views.bunchOfKey_view.as_view(), name='bunchOfKey'),
]