from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdminOrVolunteerAllowed
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

    def get(self, _request: Request, id: UUID) -> Response:
        user = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, id: UUID) -> Response:
        user = UserProfile.objects.get(id=id)
        user.delete()
        return Response(
            {"statusCode": 200, "message": "User deleted successfully"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, id: UUID) -> Response:
        user = UserProfile.objects.get(id=id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminOrVolunteerAllowed,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("role",)
    ordering_fields = ("user__date_joined",)
    ordering = ("-user__date_joined",)

    def get_queryset(self) -> UserProfile:
        queryset = UserProfile.objects.all()
        role = self.request.query_params.get("role", None)
        if not self.request.user.is_superuser:
            user_profile = UserProfile.objects.get(user_id=self.request.user.id)
            if user_profile.role == "volunteer":
                role = "adopter"
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        if request.user.is_superuser:
            user_data = {
                "role": "admin",
                "user": {
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                },
            }
            return Response(user_data, status=status.HTTP_200_OK)
        user = UserProfile.objects.get(user_id=request.user.id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        user = UserProfile.objects.get(user_id=request.user.id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
