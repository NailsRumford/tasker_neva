from django.shortcuts import render
from service_zones.forms import ServiceZoneForm
from .models import Engineer
from django.shortcuts import get_object_or_404, redirect
from service_zones.models import ServiceZone
from core.decorators.user_decorators import engineer_required
from django.db.models import Q
from technicians.models import Technician

@engineer_required
def index(request):
    template = 'engineers/service_zones.html'
    context = {'form': ServiceZoneForm()}
    return render(request, template_name=template, context=context)


@engineer_required
def service_zones(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.filter(branch = engineer.branch)
    branch_location = engineer.branch.get_location()
    template = 'engineers/service_zones.html'
    context = {'zones': zones,
               'branch_location': branch_location}
    return render(request, template_name=template, context=context)


@engineer_required
def create_service_zone(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.filter(branch = engineer.branch)
    branch_location = engineer.branch.get_location()
    form = ServiceZoneForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        service_zone = form.save(commit=False)
        service_zone.geopoints = form.cleaned_data['geopoints']
        service_zone.branch = engineer.branch
        service_zone.save()
        return redirect('engineers:service_zones')

    return render(request,
                  'engineers/create_service_zone.html',
                  {'form': form,
                   'zones': zones,
                   'branch_location': branch_location})


@engineer_required
def service_zone_edit(request, service_zone_id):
    zone = get_object_or_404(ServiceZone, id=service_zone_id)
    zones = ServiceZone.objects.filter(Q(branch=zone.branch) & ~Q(id=zone.id))
    engineer = get_object_or_404(Engineer, user=request.user)
    branch_location = engineer.branch.get_location()
    template_create = 'engineers/create_service_zone.html'
    form = ServiceZoneForm(request.POST or None, instance=zone)
    if form.is_valid():
        form.save()
        return redirect('engineers:service_zones')
    context = {
        'form': form,
        'is_edit': True,
        'zones': zones,
        'zone': zone,
        'branch_location': branch_location
    }

    return render(request, template_create, context)


@engineer_required
def service_zone_delete(request, service_zone_id):
    service_zone = get_object_or_404(ServiceZone, id=service_zone_id)
    service_zone.delete()
    return redirect('engineers:service_zones')



@engineer_required
def technicians(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    technicians = Technician.objects.filter(branch =engineer.branch)
    template = 'engineers/technicians.html'
    context = {'technicians': technicians}
    return render (request, template, context)

def technician_activate(request, technician_id):
    technician = get_object_or_404(Technician, id = technician_id)
    technician.is_active = True
    technician.save()
    return redirect('engineers:technicians')

def technician_deactivate(request, technician_id):
    technician = get_object_or_404(Technician, id = technician_id)
    technician.is_active = False
    technician.save()
    return redirect('engineers:technicians')

def technician_detail(request, technician_id):
    technician = get_object_or_404(Technician, id = technician_id)
    