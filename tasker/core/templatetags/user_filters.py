from django import template
from fire_alarm_objects.models import FireAlarmObject
from datetime import datetime, timedelta
from django.template.loader import render_to_string
register = template.Library()


@register.filter
def addclass(field, css):
    """Добавляет в field  атрибут css"""
    return field.as_widget(attrs={'class': css})

@register.filter
def add_object_balloon(object):
    context = {
        'object': object,
    }

    balloon_content = render_to_string('technicians/includes/map_balloon_content.html', context)
    balloon_content =  balloon_content.replace(" ", "").replace("\n", "").strip()
    return f'{balloon_content}'


@register.filter
def map_icon_color(object: FireAlarmObject):
    
    delta = object.next_service_date - datetime.now().date()
    if delta.days <= 3:
        return '#A52A2A'
    elif delta.days <= 6:
        return '#FFD700'
    elif delta.days <= 9:
        return '#0000FF'
    else:
        return '#808080'
    
@register.filter    
def get_monthly_service_count(objects):
    return objects.filter(frequency='Ежемесячно').count()

@register.filter
def get_quarterly_service_count(objects):
    return objects.filter(frequency='Ежеквартально').count()


@register.filter
def get_zone_quarterly_service_count(objects, zone):
    return objects.filter(frequency='Ежеквартально', zone = zone).count()