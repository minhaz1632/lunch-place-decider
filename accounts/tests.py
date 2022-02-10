import pytest
from faker import Faker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from rest_framework import status
from django.contrib.auth.models import User

from accounts.data import DefaultUserGroups
from accounts.views import UserAuthViewSet

faker: Faker = Faker()


def get_signup_data():
    profile_dict = {}
    profile = faker.profile()
    profile_dict["first_name"], profile_dict["last_name"] = profile.get("name").split(
        " ", 1
    )
    profile_dict["username"] = profile.get("username")
    profile_dict["email"] = profile.get("mail")
    profile_dict["password"] = faker.password()
    profile_dict["password_confirmation"] = profile_dict["password"]

    return profile_dict


@pytest.mark.django_db
class TestAccountSignup:
    @pytest.mark.parametrize(
        "user_group",
        [
            DefaultUserGroups.OFFICE_EMPLOYEE.value,
            DefaultUserGroups.RESTAURANT_OWNER.value,
        ],
    )
    def test_user_signup(self, user_group):
        user_instance = UserAuthViewSet.user_signup(get_signup_data(), user_group)

        assert user_instance.groups.filter(name=user_group).exists()

    @pytest.mark.parametrize(
        "user_group",
        [
            DefaultUserGroups.OFFICE_EMPLOYEE.value,
            DefaultUserGroups.RESTAURANT_OWNER.value,
        ],
    )
    def test_user_login(self, user_group):
        user_data = get_signup_data()
        UserAuthViewSet.user_signup(user_data, user_group)
        token, created = UserAuthViewSet.user_login(
            {
                "username": user_data.get("username"),
                "password": user_data.get("password"),
            },
            user_group,
        )

        assert token is not None

    @pytest.mark.parametrize(
        "user_group, user_exists",
        [
            (DefaultUserGroups.OFFICE_EMPLOYEE.value, True),
            (DefaultUserGroups.RESTAURANT_OWNER.value, False),
        ],
    )
    def test_employee_signup(self, user_group, user_exists):
        user_data = get_signup_data()
        client = APIClient()
        url = reverse("user_auth-employee_signup")
        client.post(url, data=user_data)
        user = User.objects.get(username=user_data.get("username"))

        assert user.groups.filter(name=user_group).exists() is user_exists

    @pytest.mark.parametrize(
        "user_group, login_should_succeed",
        [
            (DefaultUserGroups.OFFICE_EMPLOYEE.value, True),
            (DefaultUserGroups.RESTAURANT_OWNER.value, False),
        ],
    )
    def test_employee_login(self, user_group, login_should_succeed):
        user_data = get_signup_data()
        login_data = {
            "username": user_data.get("username"),
            "password": user_data.get("password"),
        }
        UserAuthViewSet.user_signup(user_data, user_group)
        client = APIClient()
        url = reverse("user_auth-employee_login")
        response = client.post(url, data=login_data)
        expected_status_code = (
            status.HTTP_200_OK if login_should_succeed else status.HTTP_403_FORBIDDEN
        )

        assert response.status_code == expected_status_code

    @pytest.mark.parametrize(
        "user_group, user_exists",
        [
            (DefaultUserGroups.OFFICE_EMPLOYEE.value, False),
            (DefaultUserGroups.RESTAURANT_OWNER.value, True),
        ],
    )
    def test_restaurant_signup(self, user_group, user_exists):
        user_data = get_signup_data()
        client = APIClient()
        url = reverse("user_auth-restaurant_signup")
        client.post(url, data=user_data)
        user = User.objects.get(username=user_data.get("username"))

        assert user.groups.filter(name=user_group).exists() is user_exists

    @pytest.mark.parametrize(
        "user_group, login_should_succeed",
        [
            (DefaultUserGroups.OFFICE_EMPLOYEE.value, False),
            (DefaultUserGroups.RESTAURANT_OWNER.value, True),
        ],
    )
    def test_restaurant_login(self, user_group, login_should_succeed):
        user_data = get_signup_data()
        login_data = {
            "username": user_data.get("username"),
            "password": user_data.get("password"),
        }
        UserAuthViewSet.user_signup(user_data, user_group)
        client = APIClient()
        url = reverse("user_auth-restaurant_login")
        response = client.post(url, data=login_data)
        expected_status_code = (
            status.HTTP_200_OK if login_should_succeed else status.HTTP_403_FORBIDDEN
        )

        assert response.status_code == expected_status_code
