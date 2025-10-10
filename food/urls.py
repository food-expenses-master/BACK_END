from django.urls import path
from .views import FoodListGenericAPIView

urlpatterns = [
    path("", FoodListGenericAPIView.as_view()),
]
