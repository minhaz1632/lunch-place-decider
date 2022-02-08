from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsRestaurantOwner
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class RestaurantModelViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)