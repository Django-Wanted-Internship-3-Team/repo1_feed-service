from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    UserConfirmCodeSerializer,
    UserConfirmSerializer,
    UserSerializer,
)


class SignupView(APIView):
    @swagger_auto_schema(
        operation_summary="유저 회원가입",
        request_body=UserConfirmCodeSerializer,
        responses={
            status.HTTP_201_CREATED: UserConfirmCodeSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """
        username, email, paswword를 받아 유저 계정과 인증 코드를 생성합니다.
        Args:
            email: 이메일
            username: 이름
            password: 비밀번호
        Returns:
            email: 생성된 계정 이메일
            username: 생성된 계정 이름
            code: 생성된 인증 코드
        """
        serializer = UserConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_confirm_code = serializer.save()

        response_data = UserSerializer(user_confirm_code.user).data
        response_data["confirm_code"] = user_confirm_code.code
        return Response(response_data, status=status.HTTP_201_CREATED)


class ConfirmUserView(APIView):
    @swagger_auto_schema(
        operation_summary="유저 가입 승인",
        request_body=UserConfirmSerializer,
        responses={
            status.HTTP_200_OK: UserConfirmSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """
        username, paswword, code를 받아 code가 user의 인증코드와 같을 경우 회원가입을 승인합니다.
        Args:
            username: 이름
            password: 비밀번호
            code: 인증 코드
        Returns:
            username: 이름
            is_confirmed: 인증 여부
        """
        user = get_object_or_404(get_user_model(), username=request.data["username"])
        serializer = UserConfirmSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {}
        response_data["username"] = user.username
        response_data["is_confirmed"] = user.is_confirmed

        return Response(response_data, status=status.HTTP_200_OK)
