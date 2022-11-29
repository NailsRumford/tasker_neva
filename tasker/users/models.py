from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    RANK_PERSON = (('A', 'Админ базы данных'),
            ('E', 'Инженер'),
            ('R', 'Техник'),
            ('S', 'Обследовальщик'),
            ('F', 'Монтажник'))
    rank = models.CharField(max_length=1, choices=RANK_PERSON )
