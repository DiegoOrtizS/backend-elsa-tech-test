from rest_framework import serializers

from api.animal.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["id", "name", "age", "breed", "pet_type", "status"]
        read_only_fields = ["id"]
