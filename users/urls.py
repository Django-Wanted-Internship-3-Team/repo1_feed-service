from django.urls import path

from users.views import ConfirmUserView, SignupView

urlpatterns = [path("signup/", SignupView.as_view(), name="signup"), path("confirm/", ConfirmUserView.as_view(), name="confirm")]
