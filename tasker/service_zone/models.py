from django.db import models
from branch.models import Branch
from technicians.models import Technician


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

    class Meta:
        verbose_name = 'зона обслуживания'
        verbose_name_plural = 'зоны обслуживания'


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
