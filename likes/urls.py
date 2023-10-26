from django.urls import path

from . import views

urlpatterns = [
    path("<str:content_id>/", views.LikesAPIView.as_view()),
]
