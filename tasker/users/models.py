from django.db import models
from django.contrib.auth.models import AbstractUser

RANK =(('A','Админ базы данных'),
       ('E','Инженер'),
       ('R','Техник'),
       ('S','Обследовальщик'),
       ('F','Монтажник'))


class User(AbstractUser):
    rank = models.CharField(max_length=1, choices=RANK)

