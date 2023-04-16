from django.shortcuts import render
from service_zones.forms import ServiceZoneForm, AssignZonesForm
from .models import Engineer
from django.shortcuts import get_object_or_404, redirect
from service_zones.models import ServiceZone, TechnicianZone
from core.decorators.user_decorators import engineer_required
from django.db.models import Q
from technicians.models import Technician
from fire_alarm_objects.models import FireAlarmObject
from fire_alarm_objects.forms import FireAlarmObjectForm, AddZone2FireAlarmObjectForm
from shapely.geometry import Polygon
import csv
from django.shortcuts import render
from core.tools.tools_for_addrees import clean_address, clean_date
from service_оrganizations.models import ServiceOrganizations
from django.db.models import Prefetch
from .tools.objects import get_fire_alarm_objects
from core.tools.tools import days_left_in_month
from fire_alarm_objects.models import FailedService, FireAlarmObject, FireAlarmObjectService


@engineer_required
def index(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.filter(branch=engineer.branch)
    fire_alarm_objects = FireAlarmObject.objects.select_related(
        'address').filter(branch=engineer.branch)
    branch_location = engineer.branch.get_location()
    template = 'engineers/index.html'
    context = {'zones': zones,
               'branch_location': branch_location,
               'objects': fire_alarm_objects}
    return render(request, template_name=template, context=context)


@engineer_required
def service_zones(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.filter(branch=engineer.branch)
    fire_alarm_objects = FireAlarmObject.objects.select_related(
        'address').filter(branch=engineer.branch)
    branch_location = engineer.branch.get_location()
    template = 'engineers/service_zones.html'
    context = {'zones': zones,
               'branch_location': branch_location,
               'objects': fire_alarm_objects}
    return render(request, template_name=template, context=context)


@engineer_required
def create_service_zone(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    zones = ServiceZone.objects.filter(branch=engineer.branch)
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


def get_full_technicians(branch):
    technicians = Technician.objects.filter(branch=branch)
    result = []
    for technician in technicians:
        service_zones = ServiceZone.objects.filter(
            technicians__technician_id=technician.id)
        fire_alarm_objects = FireAlarmObject.objects.select_related(
            'address').filter(service_zone__technicians__technician_id=technician.id)
        result.append({
            'technician': technician,
            'service_zones': service_zones,
            'fire_alarm_objects': fire_alarm_objects,
            'branch_location': technician.branch.get_location()
        })
    return result


@engineer_required
def technicians(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    technicians = get_full_technicians(branch=engineer.branch)
    template = 'engineers/technicians.html'
    context = {'technicians_obj_list': technicians,
               'show_map': True}
    return render(request, template, context)


@engineer_required
def technician_activate(request, technician_id):
    technician = get_object_or_404(Technician, id=technician_id)
    technician.is_active = True
    technician.save()
    return redirect('engineers:technician_detail', technician_id)


@engineer_required
def technician_deactivate(request, technician_id):
    technician = get_object_or_404(Technician, id=technician_id)
    technician.is_active = False
    technician.save()
    return redirect('engineers:technician_detail', technician_id)


@engineer_required
def assign_zones(request, technician_id):
    technician = Technician.objects.get(id=technician_id)
    if request.method == 'POST':
        form = AssignZonesForm(technician, request.POST)
        if form.is_valid():
            form.save()
            return redirect('technician_detail', technician_id=technician_id)
    else:
        form = AssignZonesForm(technician)
    return render(request, 'assign_zones.html', {'form': form, 'technician': technician})


@engineer_required
def technician_detail(request, technician_id):
    technician = get_object_or_404(Technician, id=technician_id)
    technician_zones = TechnicianZone.objects.filter(technician=technician)
    fire_alarm_objects = FireAlarmObject.objects.select_related(
        'address').filter(
        service_zone__technicians__technician_id=technician.id)
    service_zones = ServiceZone.objects.select_related('fire_alarm_objects').filter(
        technicians__technician_id=technician.id).select_related
    if request.method == 'POST':
        form = AssignZonesForm(technician, request.POST)
        if form.is_valid():
            form.save()
            return redirect('engineers:technician_detail', technician_id)
    form = AssignZonesForm(technician)
    return render(request, 'engineers/technician.html', {'technician': technician,
                                                         'branch_location': technician.branch.get_location(),
                                                         'form': form,
                                                         'technician_zone': technician_zones,
                                                         'service_zones': service_zones,
                                                         'fire_alarm_objects': fire_alarm_objects,
                                                         'show_info': True})


@engineer_required
def technician_zone_delete(request, technician_zone_id):
    technician_zone = TechnicianZone.objects.select_related(
        'technician').get(id=technician_zone_id)
    technician_id = technician_zone.technician.id
    technician_zone.delete()
    return redirect('engineers:technician_detail', technician_id)


@engineer_required
def fire_alarm_objects(request):
    fire_alarm_objects = FireAlarmObject.objects.all()
    engineer = get_object_or_404(Engineer, user=request.user)
    branch_location = engineer.branch.get_location()
    service_zones = ServiceZone.objects.filter(branch=engineer.branch)
    context = {'fire_alarm_objects': fire_alarm_objects,
               'branch_location': branch_location,
               'service_zones': service_zones,
               'days_left_in_month': days_left_in_month()}
    template = 'engineers/fire_alarm_objects.html'
    return render(request, template, context)


@engineer_required
def fire_alarm_objects_filter(request, to_date=None):
    fire_alarm_objects = get_fire_alarm_objects(request, to_date)
    engineer = get_object_or_404(Engineer, user=request.user)
    branch_location = engineer.branch.get_location()
    service_zones = ServiceZone.objects.filter(branch=engineer.branch)

    context = {'fire_alarm_objects': fire_alarm_objects,
               'branch_location': branch_location,
               'service_zones': service_zones,
               'days_left_in_month': days_left_in_month()}
    template = 'engineers/fire_alarm_objects.html'
    return render(request, template, context)


@engineer_required
def create_fire_alarm_object(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    fire_alarm_object_form = FireAlarmObjectForm(
        engineer, request.POST or None, files=request.FILES or None,)

    if fire_alarm_object_form.is_valid():
        fire_alarm_object = fire_alarm_object_form.save(commit=False)
        fire_alarm_object.branch = engineer.branch
        fire_alarm_object.auto_add_service_zone()
        fire_alarm_object.save()
        if fire_alarm_object.service_zone:
            return redirect('engineers:fire_alarm_object_detail', fire_alarm_object.id)
        return redirect('engineers:fire_alarm_object_detail', fire_alarm_object.id)
    template = 'engineers/fire_alarm_object/create_fire_alarm_object.html'
    context = {'fire_alarm_object_form': fire_alarm_object_form}
    return render(request, template, context)


@engineer_required
def fire_alarm_object_delete(request, object_id):
    engineer = get_object_or_404(Engineer, user=request.user)
    fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
    fire_alarm_object.delete()
    return redirect('engineers:fire_alarm_objects')


@engineer_required
def add_zone2fire_alarm_object_form(request, fire_alarm_object):
    engineer = get_object_or_404(Engineer, user=request.user)
    add_zone2fire_alarm_object_form = AddZone2FireAlarmObjectForm(request.POST or None,
                                                                  instance=fire_alarm_object,
                                                                  engineer=engineer)
    if add_zone2fire_alarm_object_form.is_valid():
        fire_alarm_object = add_zone2fire_alarm_object_form.save()
        fire_alarm_object.save()
        return redirect('engineers:fire_alarm_object_detail', fire_alarm_object.id)
    return add_zone2fire_alarm_object_form


@engineer_required
def fire_alarm_object_detail(request, object_id):
    fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
    zone2fire_alarm_object_form = add_zone2fire_alarm_object_form(
        request, fire_alarm_object)
    fire_alarm_object_services = FireAlarmObjectService.objects.filter(
        fire_alarm_object_id=object_id).order_by('-service_date')
    fire_alarm_object_failed_services = FailedService.objects.filter(fire_alarm_object_id=object_id).exclude(
        Q(status='completed')).order_by('-service_date')
    context = {
        'fire_alarm_object': fire_alarm_object,
        'fire_alarm_object_services': fire_alarm_object_services,
        'fire_alarm_object_failed_services': fire_alarm_object_failed_services,
        'show_delete': True,
        'days_left_in_month': days_left_in_month(),
        'add_zone2fire_alarm_object_form': zone2fire_alarm_object_form}
    template = 'engineers/fire_alarm_object_detail.html'
    return render(request, template, context)


@engineer_required
def import_csv(request):
    engineer = get_object_or_404(Engineer, user=request.user)
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        success_count = 0
        error_count = 0
        double_count = 0
        error_list = []
        for row in reader:
            try:
                address = clean_address(row['address'])
                name = row['name']
                frequency = row['frequency']
                if frequency != 'Ежемесячно' and frequency != 'Ежеквартально':
                    error_list.append(
                        f'Неправильно указан {frequency}, для {name}, {address}')
                    raise Exception
                last_service_date = clean_date(row['last_service_date'])
                service_organizations = row['service_organizations ']
                if not ServiceOrganizations.objects.filter(name=service_organizations).exists():
                    error_list.append(
                        f'Не существует сервисной организации {service_organizations}. Объект {name}, {address} будет создан без сервесной организации ')
                service_organizations = ServiceOrganizations.objects.get(
                    name=service_organizations)
                model, status = FireAlarmObject.objects.get_or_create(name=name,
                                                                      address=address,
                                                                      frequency=frequency,
                                                                      last_service_date=last_service_date,
                                                                      branch=engineer.branch,
                                                                      service_organizations=service_organizations)
                if status:
                    success_count += 1
                    status = model.auto_add_service_zone()
                    if not status:
                        error_list.append(
                            f'Для объект {name}, {address} неполучилось назначить зону')
                else:
                    double_count += 1

            except Exception as ex:
                error_count += 1
                address = row['address']
                name = row['name']
                error_list.append(
                    f'Не удалось добавить: {name} c адрессом :{address}')

        return render(request, 'engineers/import_csv.html', {'success_count': success_count,
                                                             'error_count': error_count,
                                                             'error_list': error_list,
                                                             'double_count': double_count})
    else:
        return render(request, 'engineers/import_csv.html')
