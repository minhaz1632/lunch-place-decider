import django_filters
from restaurants.models import RestaurantMenu


class RestaurantMenuFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = RestaurantMenu
        fields = ["date", "restaurant"]
