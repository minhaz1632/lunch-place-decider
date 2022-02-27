from datetime import date
from django.db.models import Count, F
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action

from accounts.permissions import IsOfficeEmployee
from polls.models import Polls
from polls.serializers import PollsSerializer, WinnerMenuSerializer


class PollsViewSet(GenericViewSet, CreateModelMixin):
    permission_classes = [IsOfficeEmployee]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        if self.action == "winner":
            return WinnerMenuSerializer

        return PollsSerializer

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
            .filter(restaurant_menu__date=date.today())
            .order_by(F("polls_count").desc())
            .first()
        )

        return Response(WinnerMenuSerializer(winner).data)
