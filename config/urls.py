from rest_framework import permissions

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="소셜 미디어 통합 Feed 서비스",
        default_version="v1",
        description="원티드 프리온보딩 과제 1",
        contact=openapi.Contact(email="wogur981208@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API
    path("api/posts/", include("posts.urls")),
    path("api/common/", include("common.urls")),
    # Swagger
    path("swagger/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # Likes
    path("api/likes/", include("likes.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
