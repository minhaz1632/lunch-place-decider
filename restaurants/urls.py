from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.views import RestaurantModelViewSet

restaurant_view_router = DefaultRouter()
restaurant_view_router.register("", RestaurantModelViewSet, basename="restaurants")

urlpatterns = [
    path("", include(restaurant_view_router.urls)),
]
