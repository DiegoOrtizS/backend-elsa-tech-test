from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.user.models import UserProfile
from api.user.serializers import UserProfileSerializer


class UserView(APIView, ListModelMixin):
    permission_classes = (IsAdminUser,)

    error_message = {"success": False, "msg": "Error updating user"}

    def post(self, request: Request) -> Response:
        serializer: UserProfileSerializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data = serializer.data
        refresh = RefreshToken.for_user(account)
        data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore[attr-defined]
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, _request: Request, id: int | None = None) -> Response:
        if id:
            # Fetch user by ID
            try:
                user = UserProfile.objects.get(id=id)
            except UserProfile.DoesNotExist:
                return Response(
                    {"success": False, "msg": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserProfileSerializer(user)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, id: int | None = None) -> Response:
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response(
                {"success": False, "msg": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.delete()
        return Response(
            {"success": True, "msg": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
