import pytest
from faker import Faker

from accounts.data import DefaultUserGroups
from accounts.views import UserAuthViewSet
"""
1. Signup Restaurant and Office employees
2. Login and vice versa
3. Logout and vice versa
4. user_logout
5. user_login
6. user_signup
"""

faker: Faker = Faker()
# account_fields = [
    #     "username",
    #     "first_name",
    #     "last_name",
    #     "email",
    #     "password",
    #     "password_confirmation",
    # ]


def get_signup_data():
    profile_dict = {}
    profile = faker.profile()
    profile_dict['first_name'], profile_dict['last_name'] = profile.get('name').split(' ', 1)
    profile_dict['username'] = profile.get('username')
    profile_dict['email'] = profile.get('mail')
    profile_dict['password'] = faker.password()
    profile_dict['password_confirmation'] = profile_dict['password']

    return profile_dict


class TestAccountSignup:
    @pytest.mark.django_db
    @pytest.mark.parametrize('user_group', [DefaultUserGroups.OFFICE_EMPLOYEE.value, DefaultUserGroups.RESTAURANT_OWNER.value])
    def test_user_signup(self, user_group):
        user_instance = UserAuthViewSet.user_signup(get_signup_data(), user_group)

        assert user_instance.groups.filter(
                name=user_group
            ).exists()
