from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.user.models import UserProfile
from api.user.serializers import UserProfileSerializer


class UserView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request: Request) -> Response:
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data = serializer.data
        refresh = RefreshToken.for_user(account)
        data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),  # type: ignore[attr-defined]
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, _request: Request, id: str) -> Response:
        user = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, id: str) -> Response:
        user = UserProfile.objects.get(id=id)
        user.delete()
        return Response(
            {"statusCode": 200, "message": "User deleted successfully"},
            status=status.HTTP_200_OK,
        )
