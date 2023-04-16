from django.shortcuts import get_object_or_404
from fire_alarm_objects.models import FireAlarmObject
from django.utils import timezone
from django.db.models import Q
from engineers.models import Engineer

def get_fire_alarm_objects(request, to_date):
    engineer = get_object_or_404(Engineer, user = request.user)
    fire_alarm_objects = FireAlarmObject.objects.filter(
        Q(branch=engineer.branch) &
        Q(next_service_date__lte=timezone.now() + timezone.timedelta(days=to_date)))
    return fire_alarm_objects