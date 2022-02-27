from django.db import models
from django.contrib.auth.models import User

from restaurants.models import RestaurantMenu


class Polls(models.Model):
    restaurant_menu = models.ForeignKey(RestaurantMenu, on_delete=models.PROTECT)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "polls"
        unique_together = ["restaurant_menu", "employee"]
