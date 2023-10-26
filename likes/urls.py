from django.urls import path

from . import views

urlpatterns = [
    path("<int:content_id>/", views.LikesAPIView.as_view()),
]
