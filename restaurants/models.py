from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        db_table = "restaurant"


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "restaurant_menu"
        unique_together = ["date", "restaurant_id"]
        ordering = ["-date"]
