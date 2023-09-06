from rest_framework.permissions import BasePermission


class IsUnauthorized(BasePermission):
    """
    Allows access only to unauthorized users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)