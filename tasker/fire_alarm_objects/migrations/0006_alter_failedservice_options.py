# Generated by Django 4.1.7 on 2023-04-26 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fire_alarm_objects', '0005_firealarmobject_contract_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='failedservice',
            options={'verbose_name': 'Проблема с обслуживания', 'verbose_name_plural': 'Проблемы с обслуживаниями'},
        ),
    ]
