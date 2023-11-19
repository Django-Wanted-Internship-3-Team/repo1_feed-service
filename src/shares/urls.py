from django.urls import path

from shares.views import SharesAPIView

urlpatterns = [
    path("<str:content_id>/", SharesAPIView.as_view(), name="shares"),
]
