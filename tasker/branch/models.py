from django.db import models

class Branch(models.Model):
    """
    Модель для хранения информации о филиалах.
    """
    name = models.CharField(
        max_length=50,
        verbose_name=_('название'),  # Verbose name для поля name
        help_text=_('Введите название филиала'),  # Help text для поля name
    )

    class Meta:
        verbose_name = _('филиал')  # Verbose name для модели Branch
        # Verbose name во множественном числе для модели Branch
        verbose_name_plural = _('филиалы')

    def __str__(self):
        return self.name
