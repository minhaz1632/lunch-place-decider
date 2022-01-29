from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "restaurant"


class EmployeeRestaurant(models.Model):
    user = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "employee_restaurant"
