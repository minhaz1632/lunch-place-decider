from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from accounts.views import UserAuthViewSet

user_auth_view_router = DefaultRouter()
user_auth_view_router.register('', UserAuthViewSet, basename='employee_auth')

urlpatterns = [
    path('', include(user_auth_view_router.urls)),
]
