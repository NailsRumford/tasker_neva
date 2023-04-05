from django.db import models
from django.contrib.auth import get_user_model
from branches.models import Branch
User = get_user_model()


class Engineer(models.Model):
    """
    Модель для хранения информации об инженерах.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Пользователь, к которому относится инженер',
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='филиал',
        help_text='Выберите филиал, к которому относится инженер'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='активен',
        help_text='Укажите, активена ли учетная запись инженер',
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия',
        help_text='Фамилия инженера',
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='имя',
        help_text='Имя инженера',
    )
    middle_name = models.CharField(
        max_length=30,
        verbose_name='отчество',
        help_text='Отчество инженера',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='телефон',
        help_text='Телефон инженера',
    )
    photo = models.ImageField(
        upload_to='engineer_photos',
        blank=True,
        null=True,
        verbose_name='фото',
        help_text='Фото инженера',
    )

    class Meta:
        verbose_name = 'инженер'
        verbose_name_plural = 'инженеры'

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"