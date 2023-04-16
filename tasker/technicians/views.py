from django.shortcuts import render
from core.decorators.user_decorators import technician_required
from django.shortcuts import get_object_or_404, redirect
from .models import Technician
from fire_alarm_objects.models import FireAlarmObject, FireAlarmObjectService, FailedService
from django.db.models import Q
from django.utils import timezone
from fire_alarm_objects.forms import FireAlarmObjectServiceForm, FailedServiceForm
import datetime
import calendar


@technician_required
def index(request):
    technician = get_object_or_404(Technician, user=request.user)
    branch_location = technician.branch.get_location()
    fire_alarm_objects = FireAlarmObject.objects.select_related(
        'address').filter(
        service_zone__technicians__technician_id=technician.id)
    template = "technicians/index.html"

    context = {'objects': fire_alarm_objects,
               'branch_location': branch_location,
               'mobi': True,
               'days_left_in_month': days_left_in_month()}
    return render(request, template, context)


def days_left_in_month():
    today = datetime.date.today()
    _, days_in_month = calendar.monthrange(today.year, today.month)
    days_left = (datetime.date(
        today.year, today.month, days_in_month) - today).days
    return days_left


def get_fire_alarm_objects(request, to_date):
    technician = get_object_or_404(Technician, user=request.user)
    fire_alarm_objects = FireAlarmObject.objects.filter(
        Q(service_zone__technicians__technician_id=technician.id) &
        Q(next_service_date__lte=timezone.now() + timezone.timedelta(days=to_date)))
    return fire_alarm_objects


def fire_alarm_objects(request, to_date):
    technician = get_object_or_404(Technician, user=request.user)
    fire_alarm_objects = get_fire_alarm_objects(request, to_date)
    branch_location = technician.branch.get_location()
    template = "technicians/index.html"
    context = {'objects': fire_alarm_objects,
               'branch_location': branch_location,
               'mobi': True,
               'days_left_in_month': days_left_in_month()}
    return render(request, template, context)


def fire_alarm_object_service_create(request, object_id):
    form = FireAlarmObjectServiceForm(request.POST or None,
                                      files=request.FILES or None,)
    template = "technicians/fire_alarm_object_service_create.html"
    if form.is_valid():
        fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
        technician = get_object_or_404(Technician, user=request.user)
        fire_alarm_object_service = form.save(commit=False)
        fire_alarm_object_service.fire_alarm_object = fire_alarm_object
        fire_alarm_object_service.technician = technician
        fire_alarm_object_service.save()
        return redirect('technicians:index')
    fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
    technician = get_object_or_404(Technician, user=request.user)
    context = {'object': fire_alarm_object,
               'form': form,
               'mobi': True}
    return render(request, template, context)


def fire_alarm_object_service_detail(request, object_id):
    fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
    services = FireAlarmObjectService.objects.filter(
        fire_alarm_object_id=object_id).order_by('-service_date')
    failed_services = FailedService.objects.filter(fire_alarm_object_id=object_id).exclude(
        Q(status='completed')).order_by('-service_date')
    context = {
        'object': fire_alarm_object,
        'services': services,
        'failed_services': failed_services,
        'mobi': True,
    }
    return render(request, 'technicians/fire_alarm_object_service_detail.html', context)


def failed_service_create(request, object_id):
    form = FailedServiceForm(request.POST or None,
                             files=request.FILES or None,)
    fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
    technician = get_object_or_404(Technician, user=request.user)
    if form.is_valid():
        failed_service = form.save(commit=False)
        failed_service.technician = technician
        failed_service.fire_alarm_object = fire_alarm_object
        failed_service.save()
        return redirect('technicians:fire_alarm_object_service_detail', object_id)
    template = 'technicians/failed_service_create.html'
    context = {'form': form,
               'object': fire_alarm_object,
               'mobi': True, }
    return render(request, template, context)
