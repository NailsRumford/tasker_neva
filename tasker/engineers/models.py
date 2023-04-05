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

    class Meta:
        verbose_name = 'инженер'
        verbose_name_plural = 'инженеры'

    def __str__(self):
        return self.user.username
