from datetime import date
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from restaurants.models import Restaurant, RestaurantMenu
from polls.utils import is_last_two_days_winner


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "last_updated_at"]

    def create(self, validated_data):
        restaurant_instance = Restaurant(**validated_data)
        restaurant_instance.owner = self.context.get("request").user
        restaurant_instance.save()

        return restaurant_instance


class RestaurantMenuSerializer(ModelSerializer):
    class Meta:
        model = RestaurantMenu
        fields = "__all__"
        read_only_fields = ["created_at", "last_updated_at"]

    def validate(self, attrs):
        if date.today() >= attrs.get("date"):
            raise ValidationError("You can upload menu for upcoming days.")

        restaurant = attrs.get("restaurant")

        if restaurant.owner != self.context.get("request").user:
            raise ValidationError("Please select a valid restaurant.")

        if is_last_two_days_winner(restaurant.id):
            raise PermissionDenied("The winner restaurant of last two days is not eligible")

        return attrs
