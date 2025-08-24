from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint

from .manager import UserManager


class User(AbstractUser):
    username = None
    nickname = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = "nickname"

    objects = UserManager()

    class Meta:
        constraints = [
            UniqueConstraint(Lower("nickname"), name="uniq_lower_nickname")
        ]
