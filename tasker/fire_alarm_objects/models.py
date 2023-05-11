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
    
    def get_geopoint_v2(self):
        return f'{self.latitude},{self.longitude}'
    
    def get_navigator_link(self):
        return f'yandexnavi://build_route_on_map?lat_to={self.latitude}&lon_to={self.longitude}'


class FireAlarmObject(models.Model):
    FREQUENCY_CHOICES = (
        ('Ежемесячно', 'Ежемесячно'),
        ('Ежеквартально', 'Ежеквартально'),
    )

    name = models.CharField(
        max_length=500,
        verbose_name='название объекта',
        help_text='Название объекта, на котором установлена пожарная сигнализация.'
    )

    frequency = models.CharField(
        max_length=15,
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

    remote_number = models.CharField(verbose_name='Пультовый номер',
                                     max_length=20,
                                      blank=True,
                                      null=True)

    room_number = models.CharField(verbose_name='Помещение',
                                   max_length=50,
                                   blank=True,
                                   null=True)
    contract_number = models.CharField(verbose_name='Номер договора',
                                       max_length=50,
                                       blank=True,
                                       null=True)
    contract_date = models.DateField(
        verbose_name='Дата заключения договора',
        blank=True,
        null=True
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
            if self.frequency == 'Ежемесячно':
                self.next_service_date = self.last_service_date + \
                    relativedelta(months=1)
            elif self.frequency == 'Ежеквартально':
                self.next_service_date = self.last_service_date + \
                    relativedelta(months=3)
        super().save(*args, **kwargs)

    def update_next_service_date(self):
        if self.frequency == 'Ежемесячно':
            self.next_service_date = self.last_service_date + \
                relativedelta(months=1)
        elif self.frequency == 'Ежеквартально':
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
                return True
        return False


class FireAlarmObjectService(models.Model):
    """
    Модель технического обслуживания пожарной сигнализации
    """
    fire_alarm_object = models.ForeignKey(
        FireAlarmObject, on_delete=models.CASCADE, verbose_name='Объект', related_name='service_done')
    service_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    technician = models.ForeignKey(
        Technician, blank=True,
        null=True, on_delete=models.PROTECT, verbose_name='Техник', related_name='service_done')
    service_journal_title_page_photo = models.ImageField(
        upload_to='service_photos/', 
        verbose_name='Фотография обложки журнала техобслуживания ПС',
        blank=True, 
        default='media/default_image.jpg'
    )
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
            fire_alarm_object=self.fire_alarm_object, status__in=['pending', 'in_progress'])
        for failed_service in pending_failed_services:
            failed_service.status = 'completed'
            failed_service.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Обслуживание {self.fire_alarm_object} от {self.service_date}'


class FailedService(models.Model):
    """
    Модель неудавшегося обслуживания пожарной сигнализации
    """
    status_choices = [
        ('pending', 'В ожидании'),
        ('in_progress', 'Выполняется'),
        ('completed', 'Завершено'),
    ]
    technician = models.ForeignKey(
        Technician, on_delete=models.PROTECT, verbose_name='Техник', related_name='failed_services')
    status = models.CharField(choices=status_choices,
                              max_length=255, default='pending')
    service_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    fire_alarm_object = models.ForeignKey(
        FireAlarmObject, on_delete=models.CASCADE, related_name='failed_services')
    photo = models.ImageField(
        upload_to='failed_service_photos/', verbose_name='Фото неисправности', blank=True,
        null=True,)

    comment = models.TextField(verbose_name='Комментарий')
    
    class Meta:
        verbose_name = 'Проблема с обслуживания'
        verbose_name_plural = 'Проблемы с обслуживаниями'
        
    def __str__(self):
        return f"{self.fire_alarm_object} - {self.service_date }"
