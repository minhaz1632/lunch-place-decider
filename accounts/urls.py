from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserAuthViewSet

user_auth_view_router = DefaultRouter()
user_auth_view_router.register("", UserAuthViewSet, basename="user_auth")

urlpatterns = [
    path("", include(user_auth_view_router.urls)),
]
