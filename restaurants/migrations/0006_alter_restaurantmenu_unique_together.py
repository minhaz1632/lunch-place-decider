# Generated by Django 4.0.1 on 2022-02-20 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_alter_restaurantmenu_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='restaurantmenu',
            unique_together=set(),
        ),
    ]
