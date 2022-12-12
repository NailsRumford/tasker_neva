from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
# Create your models here.


class CountrySOModel(models.Model):
    """Модель записи страны в адресе"""
    name = models.CharField(
        max_length=100, verbose_name="Название страны", unique=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self) -> str:
        return f'{self.name}'


class RegionSOModel(models.Model):
    """Модель записи региона для адреса"""
    name = models.CharField(max_length=100, verbose_name="Название региона", unique=True)
    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='regions',
    )

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self) -> str:
        return f'{self.name}'


class CitySOModel(models.Model):
    """Модель записи города для адреса"""
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)
    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='citys',
    )
    region = models.ForeignKey(
        RegionSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='citys',
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self) -> str:
        return f'{self.name}'


class StreetSOModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Улица")
    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='streets',
    )
    region = models.ForeignKey(
        RegionSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='streets',

    )
    city = models.ForeignKey(
        CitySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='streets',

    )

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'

    def __str__(self) -> str:
        return f'{self.name}'


class BuildingSOModel(models.Model):
    number = models.IntegerField(verbose_name="Номер строения")
    liter = models.CharField(max_length=2, verbose_name="Литер", blank=True, null=True)
    title = str(number)+str(liter)

    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buildings',
    )
    region = models.ForeignKey(
        RegionSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buildings',
    )
    sity = models.ForeignKey(
        CitySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buildings',

    )
    street = models.ForeignKey(
        StreetSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='buildings',
    )

    class Meta:
        verbose_name = 'Строение'
        verbose_name_plural = 'Строения'

    def __str__(self) -> str:
        return f'{self.number}'


class RoomSOModel(models.Model):
    number = models.IntegerField(verbose_name="Помещение")
    liter = models.CharField(max_length=2, verbose_name="Литер")
    title = str(number)+str(liter)
    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rooms',

    )
    region = models.ForeignKey(
        RegionSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rooms',

    )
    sity = models.ForeignKey(
        CitySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rooms',

    )
    street = models.ForeignKey(
        StreetSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rooms',
    )
    building = models.ForeignKey(
        BuildingSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='rooms',
    )

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Поmeщения'

    def __str__(self) -> str:
        return f'{self.title}'


class AddressSOModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название объекта")
    country = models.ForeignKey(
        CountrySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',

    )
    region = models.ForeignKey(
        RegionSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',

    )
    sity = models.ForeignKey(
        CitySOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',

    )
    street = models.ForeignKey(
        StreetSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',
    )
    building = models.ForeignKey(
        BuildingSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',
    )
    room = models.ForeignKey(
        RoomSOModel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='object',
    )

    def __str__(self) -> str:
        return f'{self.name}'
