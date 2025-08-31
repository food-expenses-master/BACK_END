from django.urls import path
from .views import *

urlpatterns = [
    path("", UserRegisterAPIView.as_view()),
    path("sessions", UserAuthAPIView.as_view()),
]