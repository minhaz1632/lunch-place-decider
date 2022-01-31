from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "restaurant"
