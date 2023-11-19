from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import ConfirmUserView, LoginView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("confirm/", ConfirmUserView.as_view(), name="confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
