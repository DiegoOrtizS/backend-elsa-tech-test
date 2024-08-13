from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        ]
        read_only_field = ["id"]

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        password = attrs.get("password")
        if password:
            validate_password(password)
        return attrs
