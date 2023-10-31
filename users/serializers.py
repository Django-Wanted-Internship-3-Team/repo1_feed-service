from django.contrib.auth import authenticate, get_user_model, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.utils import get_random_string
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
        user = super().create(validated_data)

        confirm_code = get_random_string()
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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        if user is not None:
            refresh = TokenObtainPairSerializer.get_token(user)
            refresh["username"] = user.username
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return data
        return None

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Username or Password is Incorrect")
        if not user.is_confirmed:
            raise serializers.ValidationError("User is not confirmed yet")
        return data

    def create(self, validated_data):
        user = authenticate(username=validated_data["username"], password=validated_data["password"])
        if user is not None:
            user.is_active = True
            user.save()
        return user
