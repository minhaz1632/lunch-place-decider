# Generated by Django 4.0.1 on 2022-02-12 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_alter_restaurant_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="RestaurantMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("title", models.CharField(max_length=256)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_updated_at", models.DateTimeField(auto_now=True)),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="restaurants.restaurant",
                    ),
                ),
            ],
            options={
                "db_table": "restaurant_menu",
                "unique_together": {("date", "restaurant_id")},
            },
        ),
    ]