from django.db import models
from django.contrib.auth import get_user_model
from branches.models import Branch
User = get_user_model()


class Technician(models.Model):
    """
    Модель для хранения информации о техниках.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        help_text='Пользователь, к которому относится техник',
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
        help_text='Укажите, активена ли учетная запись техник',
    )

    class Meta:
        verbose_name = 'техник'
        verbose_name_plural = 'техники'

    def __str__(self):
        return self.user.username
