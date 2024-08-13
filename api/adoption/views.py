from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.adoption.models import Adoption
from api.adoption.serializers import AdoptionCreateUpdateSerializer, AdoptionSerializer
from api.permissions import IsAdminOrAdopterAllowed, IsAdminOrVolunteerAllowed


class AdoptionView(APIView):
    def get_permissions(self) -> list:
        if self.request.method == "POST":
            return [IsAdminOrAdopterAllowed()]
        return [IsAdminUser()]

    def post(self, request: Request) -> Response:
        serializer = AdoptionCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, _request: Request, id: UUID) -> Response:
        adoption = Adoption.objects.get(id=id)
        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _request: Request, id: UUID) -> Response:
        adoption = Adoption.objects.get(id=id)
        adoption.delete()
        return Response(
            {"statusCode": 200, "message": "Adoption deleted successfully"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, id: UUID) -> Response:
        adoption = Adoption.objects.get(id=id)
        serializer = AdoptionCreateUpdateSerializer(
            adoption, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = AdoptionSerializer
    permission_classes = (IsAdminOrVolunteerAllowed,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self) -> list[Adoption]:
        return Adoption.objects.all()
