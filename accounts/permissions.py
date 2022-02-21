from rest_framework.permissions import BasePermission
from accounts.data import DefaultUserGroups


class IsRestaurantOwner(BasePermission):
    message = "User must be a restaurant owner"

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(
                name=DefaultUserGroups.RESTAURANT_OWNER.value
            ).exists()
        )

    def has_object_permission(self, request, view, obj):
        if view.basename == "restaurant_menu":
            return obj.restaurant.owner == request.user
        else:
            return obj.owner == request.user


class IsOfficeEmployee(BasePermission):
    message = "User must be an office employee"

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(
                name=DefaultUserGroups.OFFICE_EMPLOYEE.value
            ).exists()
        )
