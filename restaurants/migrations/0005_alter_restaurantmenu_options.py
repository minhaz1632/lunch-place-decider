# Generated by Django 4.0.1 on 2022-02-13 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0004_restaurantmenu"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="restaurantmenu",
            options={"ordering": ["-date"]},
        ),
    ]
