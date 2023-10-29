import random
import string

from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

from users.models import UserConfirmCode


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


class UserConfirmCodeSerializer(UserSerializer):
    def create(self, validated_data):
        user_serializer = UserSerializer(data=validated_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        confirm_code = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        user_confirm_code = UserConfirmCode.objects.create(code=confirm_code, user=user)
        return user_confirm_code


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)
    code = serializers.CharField(max_length=32)

    def validate(self, data):
        user = self.instance
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Password is incorrect")

        if user.is_confirmed:
            raise serializers.ValidationError("User is already confirmed")

        confirm_code = UserConfirmCode.objects.get(user=user).code
        if confirm_code != data["code"]:
            raise serializers.ValidationError("Confirmation code is incorrect")

        return data

    def update(self, user, validated_data):
        user.is_confirmed = True
        user.save()
        return user
