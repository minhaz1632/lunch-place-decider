from django.contrib.auth.models import Group, User
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from accounts.serializers import AuthUserSerializer, DummySerializer
from accounts.data import DefaultUserGroups
from accounts.permissions import IsRestaurantOwner, IsOfficeEmployee


class UserAuthViewSet(ViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        if self.action in ("restaurant_login", "employee_login"):
            return AuthTokenSerializer
        elif self.action in ("restaurant_signup", "employee_signup"):
            return AuthUserSerializer
        else:
            return DummySerializer

    def get_permissions(self):
        permissions = []

        if self.action in ("restaurant_logout", "employee_logout"):
            permissions.append(IsAuthenticated())

            if self.action == "restaurant_logout":
                permissions.append(IsRestaurantOwner())
            elif self.action == "employee_logout":
                permissions.append(IsOfficeEmployee())

        return permissions

    @staticmethod
    def user_signup(data, user_group):
        serializer = AuthUserSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("password_confirmation")
        password = serializer.validated_data.pop("password")
        user_instance: User = serializer.create(
            {
                **serializer.validated_data,
            }
        )
        user_instance.set_password(password)
        user_instance.groups.add(Group.objects.get(name=user_group))
        user_instance.save()

        return user_instance

    @staticmethod
    def user_login(data, user_group):
        serializer = AuthTokenSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        if (
            User.objects.filter(
                username=serializer.validated_data.get("username"),
                groups__name__exact=user_group,
            ).exists()
            is False
        ):
            raise PermissionDenied()

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return token, created

    @staticmethod
    def user_logout(request):
        request.user.auth_token.delete()

    @action(
        methods=["post"],
        detail=False,
        url_path="employee/signup",
        url_name="employee_signup",
    )
    def employee_signup(self, request):
        """
        Signup API endpoint for office employees. Takes user data and creates an user
        instance with group name office employee.
        :param request:
        :return:
        """
        user_instance = self.user_signup(
            request.data, DefaultUserGroups.OFFICE_EMPLOYEE.value
        )
        return Response(AuthUserSerializer(user_instance).data)

    @action(
        methods=["post"],
        detail=False,
        url_path="employee/login",
        url_name="employee_login",
    )
    def employee_login(self, request):
        """
        Employee login api. Takes username and password and return token.
        :param request:
        :return:
        """
        token, _ = self.user_login(
            request.data, DefaultUserGroups.OFFICE_EMPLOYEE.value
        )
        return Response(
            {
                "token": token.key,
                "username": token.user.username,
            }
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="employee/logout",
        url_name="employee_logout",
    )
    def employee_logout(self, request):
        """
        Employee api endpoint to logout.
        :param request:
        :return:
        """
        self.user_logout(request)
        return Response("You have logged out successfully", status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        url_path="restaurant/signup",
        url_name="restaurant_signup",
    )
    def restaurant_signup(self, request):
        """
        Singup API endpoint for restaurant owners. Takes user data and creates a
        user instance with restaurant_owner group.
        :param request:
        :return:
        """
        user_instance = self.user_signup(
            request.data, DefaultUserGroups.RESTAURANT_OWNER.value
        )
        return Response(AuthUserSerializer(user_instance).data)

    @action(
        methods=["post"],
        detail=False,
        url_path="restaurant/login",
        url_name="restaurant_login",
    )
    def restaurant_login(self, request):
        """
        Restaurant employee login api. Takes username and password and return token.
        :param request:
        :return:
        """
        token, _ = self.user_login(
            request.data, DefaultUserGroups.RESTAURANT_OWNER.value
        )
        return Response(
            {
                "token": token.key,
                "username": token.user.username,
            }
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="restaurant/logout",
        url_name="restaurant_logout",
    )
    def restaurant_logout(self, request):
        """
        Restaurant api endpoint to logout.
        :param request:
        :return:
        """
        self.user_logout(request)
        return Response("You have logged out successfully", status=status.HTTP_200_OK)
