from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    nickname = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = "nickname"

    objects = UserManager()

    def __str__(self):
        return self.nickname

    class Meta:
        constraints = [
            UniqueConstraint(Lower("nickname"), name="uniq_lower_nickname")
        ]
