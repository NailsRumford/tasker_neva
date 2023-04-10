from django.db import models
import os
from django.core.files import File
from service_zones.models import ServiceZone
from branches.models import Branch
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from service_оrganizations.models import ServiceOrganizations
from shapely.geometry import Polygon, Point
from technicians.models import Technician
from tasker.settings import MEDIA_ROOT

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

    def get_geopoint(self):
        return f'[{self.latitude},{self.longitude}]'


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
        null=True,
        upload_to='service_photos/'
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
        on_delete=models.SET_NULL,
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

    class Meta:
        verbose_name = 'объект'
        verbose_name_plural = 'объекты'

    def save(self, *args, **kwargs):
        if not self.photo:
            default_image_path = os.path.join(MEDIA_ROOT, 'default_image.jpg')
            with open(default_image_path, 'rb') as f:
                default_image = File(f)
                self.photo.save('default_image.jpg', default_image, save=False)
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

    def update_next_service_date(self):
        if self.frequency == 'monthly':
            self.next_service_date = self.last_service_date + \
                relativedelta(months=1)
        elif self.frequency == 'quarterly':
            self.next_service_date = self.last_service_date + \
                relativedelta(months=3)
        self.save()

    def __str__(self):
        return self.name

    def auto_add_service_zone(self):
        geopoint = Point(eval(self.address.get_geopoint()))
        zones = ServiceZone.objects.filter(branch=self.branch)
        for zone in zones:
            if Polygon(eval(zone.geopoints)).contains(geopoint):
                self.service_zone = zone
                self.save()


class FireAlarmObjectService(models.Model):
    """
    Модель технического обслуживания пожарной сигнализации
    """
    fire_alarm_object = models.ForeignKey(
        FireAlarmObject, on_delete=models.CASCADE, verbose_name='Объект', related_name='service_done')
    service_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    technician = models.ForeignKey(
        Technician, on_delete=models.PROTECT, verbose_name='Техник', related_name='service_done')
    service_journal_photo = models.ImageField(
        upload_to='service_photos/', verbose_name='Фотография журнала техобслуживания ПС')
    control_panel_photo = models.ImageField(
        upload_to='service_photos/', verbose_name='Фотография головного прибора ПС')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Обслуживание объекта'
        verbose_name_plural = 'Обслуживания объектов'

    def save(self, *args, **kwargs):
        # при сохранении устанавливаем last_service_date на текущую дату у связанного объекта
        self.fire_alarm_object.last_service_date = timezone.now()
        self.fire_alarm_object.update_next_service_date()
        pending_failed_services = FailedService.objects.filter(
            fire_alarm=self.fire_alarm_object, status__in=['pending', 'in_progress'])
        for failed_service in pending_failed_services:
            failed_service.status = 'completed'
            failed_service.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Обслуживание {self.fire_alarm_object} от {self.service_date}'


class FailedServicePhoto(models.Model):
    photo = models.ImageField(
        upload_to='failedservices/', blank=True, null=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.photo.name


class FailedService(models.Model):
    """
    Модель неудавшегося обслуживания пожарной сигнализации
    """
    status_choices = [
        ('pending', 'В ожидании'),
        ('in_progress', 'Выполняется'),
        ('completed', 'Завершено'),
    ]
    status = models.CharField(choices=status_choices,
                              max_length=255, default='pending')
    date_created = models.DateField(default=timezone.now)
    comment = models.TextField(blank=True)
    failed_service_photos = models.ManyToManyField(FailedServicePhoto)
    fire_alarm = models.ForeignKey(FireAlarmObject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fire_alarm} - {self.date_created}"
