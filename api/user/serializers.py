from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from api.user.models import CustomUser, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
        ]
        read_only_field = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        password = attrs.get("password")
        if password:
            validate_password(password)
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ["id", "user", "role"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict) -> UserProfile:
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance: UserProfile, validated_data: dict) -> UserProfile:
        user_data = validated_data.pop("user", None)

        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
