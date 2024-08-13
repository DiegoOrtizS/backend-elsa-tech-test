from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.animal.models import Animal
from api.animal.serializers import AnimalSerializer
from api.permissions import IsAdminOrVolunteerAllowed
from api.user.models import UserProfile


class AnimalView(APIView):
    def get_permissions(self) -> list:
        if self.request.method == "PATCH":
            return [IsAdminOrVolunteerAllowed()]
        return [IsAdminUser()]

    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, _request: Request, id: UUID) -> Response:
        animal = Animal.objects.get(id=id)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, id: UUID) -> Response:
        animal = Animal.objects.get(id=id)
        animal.delete()
        return Response(
            {"statusCode": 200, "message": "Animal deleted successfully"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, id: UUID) -> Response:
        new_data = request.data
        if not self.request.user.is_superuser:
            user_profile = UserProfile.objects.get(user_id=self.request.user.id)
            if user_profile.role == "volunteer":
                new_data = {"status": request.data.get("status")}
        animal = Animal.objects.get(id=id)
        serializer = AnimalSerializer(animal, data=new_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AnimalSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("status",)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self) -> Animal:
        """
        Optionally restricts the returned animals based on the user's role.
        """
        queryset = Animal.objects.all()
        if not self.request.user.is_superuser:
            user_profile = UserProfile.objects.get(user_id=self.request.user.id)
            if user_profile.role == "adopter":
                queryset = queryset.filter(status="available")
        return queryset
