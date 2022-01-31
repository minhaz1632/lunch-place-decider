from rest_framework.serializers import ModelSerializer
from restaurants.models import Restaurant


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        read_only_fields = ['owner']

    def create(self, validated_data):
        restaurant_instance = Restaurant(**validated_data)
        restaurant_instance.owner = self.context.get('request').user
        restaurant_instance.save()

        return restaurant_instance
