from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"", views.LikesAPIViewSet, basename="recruits")

urlpatterns = [
    path("<int:content_id>/", views.LikesAPIView.as_view()),
]
# + router.urls
