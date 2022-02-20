import urllib
from datetime import date, timedelta
import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework import status
from assertpy import assert_that

from accounts.data import DefaultUserGroups
from accounts.tests import get_user_client
from restaurants.models import RestaurantMenu, Restaurant

faker: Faker = Faker()


def get_restaurant_menu_dates():
    menu_dates = []
    for num in range(10):
        menu_dates.append(date.today() + timedelta(days=num))

    return menu_dates


def create_restaurant_menu(restaurant):
    menu_dates = get_restaurant_menu_dates()
    menus = []

    for menu_date in menu_dates:
        menu_title = faker.name()
        menus.append(
            RestaurantMenu.objects.create(
                date=menu_date,
                title=menu_title,
                description=menu_title,
                restaurant=restaurant,
            )
        )

    return menus, [str(item) for item in menu_dates]


def create_restaurant(user_instance):
    restaurant = Restaurant.objects.create(name=faker.name(), owner=user_instance)
    return restaurant


@pytest.fixture(name="restaurant_menu_fixture")
def restaurant_menu_sequence():
    client, user_instance = get_user_client(DefaultUserGroups.RESTAURANT_OWNER.value)
    restaurant = create_restaurant(user_instance)
    menus, menu_dates = create_restaurant_menu(restaurant)

    return client, menus, menu_dates


@pytest.mark.django_db
class TestRestaurants:
    @pytest.mark.parametrize(
        "user_group, is_403",
        [
            (DefaultUserGroups.OFFICE_EMPLOYEE.value, True),
            (DefaultUserGroups.RESTAURANT_OWNER.value, False),
        ],
    )
    def test_view_permission(self, user_group, is_403):
        client, _ = get_user_client(user_group)
        url = reverse("restaurants-list")
        response = client.get(url)

        if is_403:
            assert response.status_code == status.HTTP_403_FORBIDDEN
        else:
            assert response.status_code == 200

    def test_restaurant_ownership_assignment(self):
        client, user_instance = get_user_client(
            DefaultUserGroups.RESTAURANT_OWNER.value
        )
        url = reverse("restaurants-list")
        response = client.post(url, {"name": faker.name()})

        assert (
            response.status_code == 201
            and response.data.get("owner") == user_instance.id
        )


@pytest.mark.django_db
class TestRestaurantMenu:
    def test_menu_date_range_filter(self, restaurant_menu_fixture):
        client, _, menu_dates = restaurant_menu_fixture
        query_data = {
            "from_date": str(menu_dates[5]),
            "to_date": str(menu_dates[9]),
        }
        url = reverse("restaurant_menu-list")
        response = client.get(f"{url}?{urllib.parse.urlencode(query_data)}")
        received_dates = [item.get("date") for item in response.data.get("results")]

        assert_that(received_dates).contains(*menu_dates[5:9]) and assert_that(
            received_dates
        ).does_not_contain(*menu_dates[0:4])

    def test_menu_date_filter(self, restaurant_menu_fixture):
        client, _, menu_dates = restaurant_menu_fixture
        query_data = {
            "date": str(menu_dates[0]),
        }
        url = reverse("restaurant_menu-list")
        response = client.get(f"{url}?{urllib.parse.urlencode(query_data)}")
        received_dates = [item.get("date") for item in response.data.get("results")]

        assert_that(received_dates).contains(menu_dates[0]) and assert_that(
            received_dates
        ).does_not_contain(*menu_dates[1:10])

    def test_menu_restaurant_filter(self):
        client, user_instance = get_user_client(
            DefaultUserGroups.RESTAURANT_OWNER.value
        )
        restaurant_1 = create_restaurant(user_instance)
        restaurant_2 = create_restaurant(user_instance)
        menus_1, _ = create_restaurant_menu(restaurant_1)
        restaurant_1_menu_dict = [
            {"name": item.title, "description": item.description} for item in menus_1
        ]
        menus_2, _ = create_restaurant_menu(restaurant_2)
        restaurant_2_menu_dict = [
            {"name": item.title, "description": item.description} for item in menus_2
        ]
        query_data = {
            "restaurant": restaurant_1.id,
        }
        url = reverse("restaurant_menu-list")
        response = client.get(f"{url}?{urllib.parse.urlencode(query_data)}")
        received_menus = [
            {"name": item.get("title"), "description": item.get("description")}
            for item in response.data.get("results")
        ]
        assert_that(received_menus).contains(*restaurant_1_menu_dict) and assert_that(
            received_menus
        ).does_not_contain(*restaurant_2_menu_dict)

    @pytest.mark.parametrize(
        "menu_date, expected_status",
        [
            (date.today(), status.HTTP_400_BAD_REQUEST),
            (date.today() + timedelta(days=-1), status.HTTP_400_BAD_REQUEST),
            (date.today() + timedelta(days=1), status.HTTP_201_CREATED),
        ],
    )
    def test_menu_creation_future_date(self, menu_date, expected_status):
        client, user_instance = get_user_client(
            DefaultUserGroups.RESTAURANT_OWNER.value
        )
        restaurant = create_restaurant(user_instance)
        url = reverse("restaurant_menu-list")
        payload = {
            "restaurant": restaurant.id,
            "date": menu_date,
            "title": faker.name(),
            "description": faker.name(),
        }

        response = client.post(url, data=payload)
        assert response.status_code == expected_status
