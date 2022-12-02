from django.db import models
from django.contrib.auth.models import AbstractUser
from .settings import RANK_PERSON


class User(AbstractUser):
    """
    Расширение базовой модели User
    RANK_PERSON объявляется в settings приложения User
    """
    rank = models.CharField(max_length=20, choices=RANK_PERSON )
    email = models.EmailField(blank=True, unique=True)
