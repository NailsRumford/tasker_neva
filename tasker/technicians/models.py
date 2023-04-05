from django.db import models
from django.contrib.auth import get_user_model
from branches.models import Branch
User = get_user_model()


class Technician(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Пользователь, к которому относится',
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='филиал',
        help_text='Выберите филиал, к которому относится техник',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='активен',
        help_text='Укажите, активена ли учетная запись',
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='имя',
        help_text='Введите имя',
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='фамилия',
        help_text='Введите фамилию',
    )
    middle_name = models.CharField(
        max_length=30,
        verbose_name='отчество',
        help_text='Введите отчество',
        blank=True,
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='телефон',
        help_text='Введите телефон',
        blank=True,
    )
    photo = models.ImageField(
        upload_to='technicians/photos/',
        verbose_name='фото',
        help_text='Выберите фото',
        blank=True,
    )

    class Meta:
        verbose_name = 'техник'
        verbose_name_plural = 'техники'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'