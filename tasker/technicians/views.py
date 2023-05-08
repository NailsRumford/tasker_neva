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
from .business_services import TechnicianIndex, TechnicianFireAlarmObjects, TechnicianFireAlarmObject


@technician_required
def index(request):
    technician = TechnicianIndex(request)
    context = technician.get_context()
    template = "technicians/index.html"
    return render(request, template, context)

def tasks(request, to_date):
    technicina= TechnicianIndex(request)
    context = technicina.get_context(to_date)
    template = "technicians/index.html"
    return render(request, template, context)

def fire_alarm_objects(request, to_date):
    technician= TechnicianFireAlarmObjects(request)
    context = technician.get_context(to_date)
    template = "technicians/fire_alarm_objects.html"
    return render(request, template, context)

def fire_alarm_object_service_detail(request, object_id):
    technician = TechnicianFireAlarmObject(request)
    context =  technician.get_context(object_id)
    template = 'technicians/fire_alarm_object_detail.html'
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
