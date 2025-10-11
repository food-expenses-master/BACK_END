from django.urls import path

from .views import FoodDetailAPIView, FoodListGenericAPIView

urlpatterns = [
    path("", FoodListGenericAPIView.as_view()),
    path("/<int:pk>", FoodDetailAPIView.as_view()),
]
