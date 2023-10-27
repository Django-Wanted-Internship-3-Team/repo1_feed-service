from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, data):
        password_validation.validate_password(data)
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data["email"], validated_data["username"], validated_data["password"])
        return user
