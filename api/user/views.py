from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.user.serializers import UserProfileSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    error_message = {"success": False, "msg": "Error updating user"}

    def post(self, request: Request) -> Response:
        serializer: UserProfileSerializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data = serializer.data
        refresh = RefreshToken.for_user(account)
        data["token"] = {"refresh": str(refresh), "access": str(refresh.access_token)}  # type: ignore[attr-defined]
        return Response(data, status=status.HTTP_201_CREATED)
