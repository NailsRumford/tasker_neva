# Generated by Django 4.1.7 on 2023-04-06 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_оrganizations', '0001_initial'),
        ('fire_alarm_objects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='firealarmobject',
            name='service_organizations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fire_alarm_objects', to='service_оrganizations.serviceorganizations', verbose_name='Обслуживающия организация'),
        ),
    ]