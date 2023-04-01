from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
from service_zone.models import ServiceZone
from branch.models import Branch
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
        default=True,
        verbose_name='активен', 
        help_text='Укажите, активена ли учетная запись инженер',
    )

    class Meta:
        verbose_name = 'инженер'
        verbose_name_plural = 'инженеры'

    def __str__(self):
        return self.user.username


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
        default=True,
        verbose_name='активен',
        help_text='Укажите, активена ли учетная запись техник',
    )

    #service_zones = models.ManyToManyField(
    #    ServiceZone,
    #    verbose_name='зоны обслуживания',
    #    help_text='Зоны обслуживания, в которых работает этот техник.',
    #    blank=True,
    #    related_name='technicians'
    #)

    class Meta:
        verbose_name = 'техник'
        verbose_name_plural = 'техники'

    def __str__(self):
        return self.user.username