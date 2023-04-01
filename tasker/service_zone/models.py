from django.db import models
from branch.models import Branch



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

    #technicians = models.ManyToManyField(
    #    Technician,
    #    verbose_name='техники',
    #    help_text='Техники, работающие в этой зоне обслуживания.',
    #    blank=True,
    #    related_name='service_zones'
    #)

    class Meta:
        verbose_name = 'зона обслуживания'
        verbose_name_plural = 'зоны обслуживания'

