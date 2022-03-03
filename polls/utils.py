from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, F
from polls.models import Polls


def is_last_two_days_winner(restaurant_id):
    for day in [timezone.localdate() - timedelta(days=1), timezone.localdate() - timedelta(days=2)]:
        winner = (
            Polls.objects.values("restaurant_menu_id", "restaurant_menu__restaurant_id")
            .annotate(polls_count=Count("restaurant_menu"))
            .filter(restaurant_menu__date=day)
            .order_by(F("polls_count").desc())
            .first()
        )

        if (
            winner is None
            or winner.get("restaurant_menu__restaurant_id") != restaurant_id
        ):
            return False

    return True
