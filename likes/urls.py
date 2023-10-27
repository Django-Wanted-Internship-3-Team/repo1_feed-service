from django.urls import path

from likes import views

urlpatterns = [
    path("<str:content_id>/", views.LikesAPIView.as_view(), name="likes"),
]
