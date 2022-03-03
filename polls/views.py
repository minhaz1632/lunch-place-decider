from django.utils import timezone
from django.db.models import Count, F
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework import status

from accounts.permissions import IsOfficeEmployee
from polls.models import Polls
from polls.serializers import PollsSerializer, WinnerMenuSerializer
from restaurants.models import RestaurantMenu
from restaurants.serializers import RestaurantMenuOptionSerializer


class PollsViewSet(GenericViewSet, CreateModelMixin):
    permission_classes = [IsOfficeEmployee]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == "winner":
            return WinnerMenuSerializer
        elif self.action == "menu_options":
            return RestaurantMenuOptionSerializer

        return PollsSerializer

    def get_queryset(self):
        return Polls.objects.filter(employee=self.request.user)

    @action(methods=["get"], detail=False)
    def menu_options(self, request):
        available_menu_options = (
            RestaurantMenu.objects.select_related("restaurant")
            .filter(date=timezone.localdate())
            .all()
        )

        if not len(available_menu_options):
            return Response("No menu available", status=status.HTTP_404_NOT_FOUND)

        data = RestaurantMenuOptionSerializer(available_menu_options, many=True).data

        return Response(data)

    @action(methods=["get"], detail=False)
    def winner(self, request):
        winner = (
            Polls.objects.values(
                "restaurant_menu__restaurant__name",
                "restaurant_menu__title",
                "restaurant_menu__description",
                "restaurant_menu_id",
            )
            .annotate(
                polls_count=Count("restaurant_menu"),
                winner_restaurant=F("restaurant_menu__restaurant__name"),
                menu_title=F("restaurant_menu__title"),
                menu_description=F("restaurant_menu__description"),
            )
            .filter(restaurant_menu__date=timezone.localdate())
            .order_by(F("polls_count").desc())
            .first()
        )

        if winner is None:
            return Response("No winner selected yet.")

        return Response(WinnerMenuSerializer(winner).data)
