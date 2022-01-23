# Generated by Django 4.0.1 on 2022-01-22 19:25

from django.db import migrations
from django.contrib.auth.models import Group
from accounts.data import DefaultUserGroups


def populate_default_user_groups(*args, **kwargs):
    for item in DefaultUserGroups:
        Group.objects.create(name=item.value)


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.RunPython(populate_default_user_groups),
    ]