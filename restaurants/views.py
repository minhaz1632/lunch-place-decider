from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsRestaurantOwner
from restaurants.models import Restaurant, RestaurantMenu
from restaurants.serializers import RestaurantSerializer, RestaurantMenuSerializer
from restaurants.filters import RestaurantMenuFilter
from restaurants.paginations import StandardResultsSetPagination


class RestaurantModelViewSet(ModelViewSet):
    """
    Crud api endpoints for the Restaurant model
    """
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class RestaurantMenuModelViewSet(ModelViewSet):
    """
    Crud api endpoints for RestaurantMenu model. The list api can be filtered with from_date,
    to_date, exact date and restaurant. It is paginated with default page size 10.
    """
    serializer_class = RestaurantMenuSerializer
    permission_classes = [IsRestaurantOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantMenuFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return RestaurantMenu.objects.filter(restaurant_id__owner=self.request.user)
