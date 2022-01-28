from rest_framework.permissions import BasePermission
from accounts.data import DefaultUserGroups


class IsRestaurantOwner(BasePermission):
    message = 'User must be a restaurant owner'

    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name=DefaultUserGroups.RESTAURANT_OWNER.value).exists()


class IsOfficeEmployee(BasePermission):
    message = 'User must be an office employee'

    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name=DefaultUserGroups.OFFICE_EMPLOYEE.value).exists()
