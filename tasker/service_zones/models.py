from django.db import models
from branches.models import Branch
from technicians.models import Technician
import random
from shapely.geometry import Polygon
from django.core.exceptions import ValidationError


class ServiceZone(models.Model):
    """
    Модель зоны обслуживания.
    """

    name = models.CharField(
        verbose_name='название',
        help_text='Название зоны обслуживания.',
        max_length=100
    )

    description = models.TextField(
        verbose_name='описание',
        help_text='Подробное описание зоны обслуживания.',
        blank=True
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='филиал',
        help_text='Филиал, к которому относится зона обслуживания.'
    )

    geopoints = models.TextField(
        verbose_name='геоточки',
        help_text='Геоточки, образующие область зоны обслуживания.'
    )

    color = models.CharField(
        verbose_name='цвет',
        help_text='Уникальный цвет зоны обслуживания.',
        max_length=10,
    )

    class Meta:
        verbose_name = 'зона обслуживания'
        verbose_name_plural = 'зоны обслуживания'

    def save(self, *args, **kwargs):
        polygon = Polygon(eval(self.geopoints))

        for zone in ServiceZone.objects.exclude(id=self.id):
            if Polygon(eval(zone.geopoints)).intersects(polygon):
                raise ValidationError(
                    f'Зоны {self.name} и {zone.name} пересекаются')
        if not self.color:
            colors = ServiceZone.objects.filter(
                branch=self.branch).values_list('color', flat=True)
            while True:
                # генерируем случайный цвет в формате #RRGGBBAA
                color = "#{:02X}{:02X}{:02X}{:02X}".format(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    0x99  # полупрозрачный
                )
                if color not in colors:
                    self.color = color
                    break
        super().save(*args, **kwargs)


class TechnicianZone (models.Model):
    technician = models.ForeignKey(
        Technician,
        verbose_name='техник',
        related_name='service_zones',
        on_delete=models.CASCADE
    )
    service_zone = models.ForeignKey(
        ServiceZone,
        verbose_name='зоны обслуживания',
        related_name='technicians',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Зона техника'
        verbose_name_plural = 'Зоны техников'
        constraints = (
            models.UniqueConstraint(
                fields=['technician', 'service_zone'], name='unique_follow'),
        )