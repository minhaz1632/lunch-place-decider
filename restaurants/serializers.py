from datetime import date
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from restaurants.models import Restaurant, RestaurantMenu


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

        return attrs


class RestaurantMenuOptionSerializer(RestaurantMenuSerializer):
    restaurant = RestaurantSerializer()
