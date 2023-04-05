from django.shortcuts import render
from service_zones.forms import ServiceZoneForm
from .models import Engineer
from django.shortcuts import get_object_or_404, redirect
from service_zones.models import ServiceZone
from core.decorators.user_decorators import engineer_required
from django.db.models import Q


@engineer_required
def index(request):
    template = 'engineers/service_zones.html'
    context = {'form': ServiceZoneForm()}
    return render(request, template_name=template, context=context)


@engineer_required
def service_zones(request):
    zones = ServiceZone.objects.all()
    template = 'engineers/service_zones.html'
    context = {'zones': zones}
    return render(request, template_name=template, context=context)


@engineer_required
def create_service_zone(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.all()
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
                   'zones': zones})


@engineer_required
def service_zone_edit(request, service_zone_id):
    zone = get_object_or_404(ServiceZone, id=service_zone_id)
    zones = ServiceZone.objects.filter(Q(branch=zone.branch) & ~Q(id=zone.id))
    template_create = 'engineers/create_service_zone.html'
    form = ServiceZoneForm(request.POST or None, instance=zone)
    if form.is_valid():
        form.save()
        return redirect('engineers:service_zones')
    context = {
        'form': form,
        'is_edit': True,
        'zones': zones,
        'zone': zone
    }

    return render(request, template_create, context)


@engineer_required
def service_zone_delete(request, service_zone_id):
    service_zone = get_object_or_404(ServiceZone, id=service_zone_id)
    service_zone.delete()
    return redirect('engineers:service_zones')
