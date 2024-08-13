from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.user.serializers import UserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    error_message = {"success": False, "msg": "Error updating user"}

    def post(self, request: Request) -> Response:
        print(request.data)
        serializer: UserSerializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data = serializer.data
        refresh = RefreshToken.for_user(account)
        data["token"] = {"refresh": str(refresh), "access": str(refresh.access_token)}  # type: ignore[attr-defined]
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request: Request) -> Response:
        serializer: UserSerializer = UserSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data: dict[str, str] = serializer.data
        return Response(data, status=status.HTTP_200_OK)
