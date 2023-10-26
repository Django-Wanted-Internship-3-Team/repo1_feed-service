from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.decorator import mandatories
from users.serializers import UserSerializer


class SignupView(APIView):
    @swagger_auto_schema(
        operation_summary="유저 회원가입",
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: UserSerializer,
        },
    )
    @mandatories("email", "username", "password")
    def post(self, request: Request, m: dict) -> Response:
        """
        username, email, paswword를 받아 유저 계정을 생성합니다.
        Args:
            email: 이메일
            username: 이름
            password: 비밀번호
        Returns:
            email: 생성된 계정 이메일
            username: 생성된 계정 이름
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
