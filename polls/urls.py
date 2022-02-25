from django.urls import path, include
from rest_framework.routers import DefaultRouter
from polls.views import PollsViewSet

router = DefaultRouter()
router.register("", PollsViewSet, basename="polls")

urlpatterns = [path("", include(router.urls))]
