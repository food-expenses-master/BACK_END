from django.urls import path
from .views import UserRegisterAPIView, UserAuthAPIView, TokenRefreshAPIView

urlpatterns = [
    path("", UserRegisterAPIView.as_view()),
    path("/auth/sessions", UserAuthAPIView.as_view()),
    path("/auth/sessions/refresh", TokenRefreshAPIView.as_view()),
]