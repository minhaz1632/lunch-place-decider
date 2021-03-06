from dateutil import relativedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polls.models import Polls
from polls.utils import is_last_two_days_winner

VOTING_DEADLINE = timezone.localtime() + relativedelta.relativedelta(hour=13, minute=0)


class PollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = "__all__"
        read_only_fields = ["employee", "created_at", "last_updated_at"]

    def validate(self, attrs):
        restaurant_menu = attrs.get("restaurant_menu")

        if timezone.localtime() > VOTING_DEADLINE:
            raise ValidationError(
                f"Voting is allowed until {VOTING_DEADLINE.strftime('%H:%M %p')}"
            )

        if restaurant_menu.date != timezone.localdate():
            raise ValidationError("You can only vote for Today's Menu")

        if is_last_two_days_winner(restaurant_menu.restaurant.id):
            raise ValidationError(
                "The winner restaurant of last two days is not eligible"
            )

        return attrs

    def create(self, validated_data):
        user = self.context.get("request").user
        polls_item = Polls.objects.filter(
            employee=user, restaurant_menu__date=timezone.localdate()
        ).first()

        if polls_item:
            for key in validated_data:
                setattr(polls_item, key, validated_data[key])
        else:
            polls_item = Polls(**validated_data)
            polls_item.employee = self.context.get("request").user
        polls_item.save()

        return polls_item


class WinnerMenuSerializer(serializers.Serializer):
    restaurant_menu_id = serializers.IntegerField()
    winner_restaurant = serializers.CharField(
        source="restaurant_menu__restaurant__name"
    )
    menu_title = serializers.CharField(source="restaurant_menu__title")
    menu_description = serializers.CharField(source="restaurant_menu__description")
    polls_count = serializers.IntegerField()
    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        return f"Voting is {'closed' if VOTING_DEADLINE < timezone.localtime() else 'still open.'}"
