from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('signup/', views.signup_view.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', TokenRefreshView.as_view(), name='login_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
