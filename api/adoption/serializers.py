from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.adoption.models import Adoption
from api.animal.models import Animal
from api.animal.serializers import AnimalSerializer
from api.user.serializers import UserSerializer

User = get_user_model()


class AdoptionSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer()
    volunteer = UserSerializer()
    adopter = UserSerializer()

    class Meta:
        model = Adoption
        fields = ["id", "created_at", "animal", "volunteer", "adopter", "status"]
        read_only_fields = ["id", "created_at", "status"]


class AdoptionCreateUpdateSerializer(serializers.ModelSerializer):
    animal_id = serializers.PrimaryKeyRelatedField(
        queryset=Animal.objects.all(), source="animal", write_only=True
    )
    volunteer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(userprofile__role="volunteer"),
        source="volunteer",
        write_only=True,
        allow_null=True,
        required=False,
    )
    adopter_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(userprofile__role="adopter"),
        source="adopter",
        write_only=True,
    )

    class Meta:
        model = Adoption
        fields = ["id", "created_at", "animal_id", "volunteer_id", "adopter_id", "status"]
        read_only_fields = ["id", "created_at"]
