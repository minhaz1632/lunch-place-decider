from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polls.models import Polls


class PollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = "__all__"
        read_only_fields = ["employee", "created_at", "last_updated_at"]

    def validate(self, attrs):
        restaurant_menu = attrs.get("restaurant_menu")

        if restaurant_menu.date != date.today():
            raise ValidationError("You can only vote for Today's Menu")

        return attrs

    def create(self, validated_data):
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
