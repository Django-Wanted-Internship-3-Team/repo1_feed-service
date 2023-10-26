from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers

from common.exceptions import InvalidPasswordException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise InvalidPasswordException(e)

        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data["email"], validated_data["username"], validated_data["password"])
        return user
