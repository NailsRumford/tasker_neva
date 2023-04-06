from django.db import models
from service_zones.models import ServiceZone
from branches.models import Branch
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from service_оrganizations.models import ServiceOrganizations


class Address(models.Model):
    """
    Модель адреса объекта
    """
    address = models.CharField(max_length=200, verbose_name="Адрес")
    latitude = models.FloatField(verbose_name="Широта", null=True, blank=True)
    longitude = models.FloatField(
        verbose_name="Долгота", null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address


class FireAlarmObject(models.Model):
    FREQUENCY_CHOICES = (
        ('monthly', 'Ежемесячно'),
        ('quarterly', 'Ежеквартально'),
    )

    name = models.CharField(
        max_length=255,
        verbose_name='название объекта',
        help_text='Название объекта, на котором установлена пожарная сигнализация.'
    )

    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        verbose_name='периодичность обслуживания',
        help_text='Периодичность обслуживания пожарной сигнализации на объекте.'
    )

    last_service_date = models.DateField(
        verbose_name='дата последнего обслуживания',
        help_text='Дата последнего обслуживания пожарной сигнализации на объекте.'
    )

    next_service_date = models.DateField(
        verbose_name='дата следующего обслуживания',
        help_text='Дата следующего обслуживания пожарной сигнализации на объекте.',
        blank=True,
        null=True
    )

    photo = models.ImageField(
        verbose_name='фото объекта',
        help_text='Фотография объекта, на котором установлена пожарная сигнализация.',
        blank=True,
        null=True
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name='Адрес объекта',
        related_name='fire_alarm_objects')

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='филиал',
        help_text='Филиал, к которому относится данный объект.',
        related_name='fire_alarm_objects'
    )

    service_zone = models.ForeignKey(
        ServiceZone,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name="Зона обслуживания",
        related_name="fire_alarm_objects")
    
    service_organizations = models.ForeignKey(
        ServiceOrganizations,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        verbose_name="Обслуживающия организация",
        related_name="fire_alarm_objects"
    )

    def save(self, *args, **kwargs):
        if not self.last_service_date:
            self.last_service_date = timezone.now().date()
        if not self.next_service_date:
            if self.frequency == 'monthly':
                self.next_service_date = self.last_service_date + \
                    relativedelta(months=1)
            elif self.frequency == 'quarterly':
                self.next_service_date = self.last_service_date + \
                    relativedelta(months=3)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name ='объект'
        verbose_name_plural ='объекты'

    def __str__(self):
        return self.name
