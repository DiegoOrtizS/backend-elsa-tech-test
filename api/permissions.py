from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.user.models import UserProfile


class IsRoleAllowed(BasePermission):
    """
    Custom permission to check if the authenticated user has a specific role.
    """

    role = None

    def has_permission(self, request: Request, _view: View) -> bool:
        auth = JWTAuthentication()
        try:
            res = auth.authenticate(request)
        except Exception as _e:
            return False

        if not res:
            return False

        user_id = res[0].id

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return False

        return user_profile.role == self.role


def get_role_permission_class(role: str) -> type:
    """
    Factory function to create a permission class for a specific role.
    """
    return type(f"Is{role.capitalize()}Allowed", (IsRoleAllowed,), {"role": role})


# Usage:
IsVolunteerAllowed = get_role_permission_class("volunteer")
IsAdopterAllowed = get_role_permission_class("adopter")


class IsAdminOrVolunteerAllowed(BasePermission):
    """
    Custom permission to check if the authenticated user is an admin or a volunteer.
    """

    def has_permission(self, request: Request, _view: View) -> bool:
        if request.user.is_superuser:
            return True

        auth = JWTAuthentication()
        try:
            res = auth.authenticate(request)
        except Exception as _e:
            return False

        if not res:
            return False

        user_id = res[0].id

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return False

        return user_profile.role == "volunteer"
