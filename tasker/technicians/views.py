from django.shortcuts import render
from core.decorators.user_decorators import technician_required
from django.shortcuts import get_object_or_404, redirect
from .models import Technician
from fire_alarm_objects.models import FireAlarmObject
from django.db.models import Q
from django.utils import timezone
from fire_alarm_objects.forms import FireAlarmObjectServiceForm


@technician_required
def index(request):
    technician = get_object_or_404(Technician, user=request.user)
    branch_location = technician.branch.get_location()
    fire_alarm_objects = FireAlarmObject.objects.select_related(
        'address').filter(
        service_zone__technicians__technician_id=technician.id)
    template = "technicians/index.html"
    form = FireAlarmObjectServiceForm()
    context = {'fire_alarm_objects': fire_alarm_objects,
               'branch_location': branch_location,
               'mobi':True}
    return render(request, template, context)


def get_fire_alarm_objects(request, to_date):
    technician = get_object_or_404(Technician, user=request.user)
    fire_alarm_objects = FireAlarmObject.objects.filter(
        Q(service_zone__technicians__technician_id=technician.id) &
        Q(next_service_date__lte=timezone.now() + timezone.timedelta(days=to_date)))
    return fire_alarm_objects


def fire_alarm_objects(request, to_date):
    fire_alarm_objects = get_fire_alarm_objects(request, to_date)
    template = "technicians/index.html"
    form = FireAlarmObjectServiceForm()
    context = {'fire_alarm_objects': fire_alarm_objects,
               'form': form}
    return render(request, template, context)


def make_service(request, object_id):
    form = FireAlarmObjectServiceForm(request.POST or None,
                                      files=request.FILES or None,)
    if form.is_valid():
        fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
        technician = get_object_or_404(Technician, user=request.user)
        fire_alarm_object_service = form.save(commit=False)
        fire_alarm_object_service.fire_alarm_object = fire_alarm_object
        fire_alarm_object_service.technician = technician
        fire_alarm_object_service.save()
        return redirect('technicians:index')
    return redirect('technicians:index')
