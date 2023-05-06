from django.db import models


class Branch(models.Model):
    """
    Модель для хранения информации о филиалах.
    """
    city = models.CharField(
        max_length=50,
        verbose_name='название',  # Verbose name для поля name
        help_text='Введите название филиала',  # Help text для поля name
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='долгота',  # Verbose name для поля longitude
        # Help text для поля longitude
        help_text='Введите долготу филиала в десятичных градусах (-180 до 180)',
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='широта',  # Verbose name для поля latitude
        # Help text для поля latitude
        help_text='Введите широту филиала в десятичных градусах (-90 до 90)',
    )
    
    class Meta:
        verbose_name = 'филиал'  # Verbose name для модели Branch
        verbose_name_plural = 'филиалы'  # Verbose name во множественном числе для модели Branch
    
    def __str__(self):
        return self.city

    def get_location(self):
        """
        Возвращает координаты филиала в виде списка [долгота, широта].

        Если значения координат не заполнены, возвращает координаты Москвы.

        :return: Список координат в формате "[долгота, широта]"
        :rtype: str
        """
        if self.longitude is not None and self.latitude is not None:
            return [self.longitude, self.latitude]
        else:
            return "[55.7522,37.6156]"
