from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class UserConfirmCode(models.Model):
    code = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_confirm_codes"

    def __str__(self):
        return f"{[self.user.email]}: {self.code}"
