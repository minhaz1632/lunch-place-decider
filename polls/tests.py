from datetime import date, timedelta
import pytest

from accounts.data import DefaultUserGroups
from accounts.tests import get_user_client
from restaurants.tests import create_restaurant, create_restaurant_menu
from polls.models import Polls
from polls.utils import is_last_two_days_winner


MENU_DATES = [date.today() - timedelta(days=1), date.today() - timedelta(days=2)]


def restaurant_menu_creation():
    _, user_instance = get_user_client(DefaultUserGroups.RESTAURANT_OWNER.value)
    restaurant = create_restaurant(user_instance)
    restaurant_menus, _ = create_restaurant_menu(restaurant, MENU_DATES)

    return restaurant, restaurant_menus


def get_employee_users():
    employees = []
    for item in range(4):
        _, user_instance = get_user_client(DefaultUserGroups.OFFICE_EMPLOYEE.value)
        employees.append(user_instance)

    return employees


@pytest.mark.django_db
def test_is_last_two_days_winner():
    employees = get_employee_users()
    winner_restaurant, winner_restaurant_menus = restaurant_menu_creation()
    loser_restaurant, loser_restaurant_menus = restaurant_menu_creation()

    for menu in winner_restaurant_menus:
        for i in range(3):
            Polls.objects.create(restaurant_menu=menu, employee=employees[i])

    for menu in loser_restaurant_menus:
        Polls.objects.create(restaurant_menu=menu, employee=employees[3])

    assert (
        is_last_two_days_winner(winner_restaurant.id) is True
        and is_last_two_days_winner(loser_restaurant.id) is False
    )
