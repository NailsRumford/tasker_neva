# Generated by Django 4.1.7 on 2023-04-26 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire_alarm_objects', '0003_firealarmobject_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firealarmobject',
            name='name',
            field=models.CharField(help_text='Название объекта, на котором установлена пожарная сигнализация.', max_length=500, verbose_name='название объекта'),
        ),
    ]
