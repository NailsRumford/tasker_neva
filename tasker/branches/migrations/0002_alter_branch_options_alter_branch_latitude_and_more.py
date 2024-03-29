# Generated by Django 4.1.7 on 2023-04-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={},
        ),
        migrations.AlterField(
            model_name='branch',
            name='latitude',
            field=models.FloatField(blank=True, help_text='Введите широту филиала в десятичных градусах (-90 до 90)', null=True, verbose_name='широта'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='longitude',
            field=models.FloatField(blank=True, help_text='Введите долготу филиала в десятичных градусах (-180 до 180)', null=True, verbose_name='долгота'),
        ),
    ]
