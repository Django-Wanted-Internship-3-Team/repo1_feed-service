from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView


class SharesAPIView(APIView):
    @swagger_auto_schema(operation_summary="게시물 좋아요")
    def post(self, request, content_id):
        pass
