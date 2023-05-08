from django.http import Http404
from typing import Dict
from .models import Technician
from fire_alarm_objects.models import FireAlarmObject, FailedService, FireAlarmObjectService
import datetime
import calendar
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect


class TechnicianSuit:
    """
    Base class for views that require a logged in Technician user.
    """

    def __init__(self, request):
        """
        Initializes the object by getting the Technician object associated with the user in the request.
        Raises Http404 if the Technician object does not exist.
        """
        self.user = request.user
        try:
            self.technician = Technician.objects.get(user=self.user)
        except Technician.DoesNotExist:
            raise Http404('Technician not found')

    def get_fire_alarm_objects(self, to_date):
        fire_alarm_objects = FireAlarmObject.objects.filter(
            Q(service_zone__technicians__technician_id=self.technician.id) &
            Q(next_service_date__lte=timezone.now() + timezone.timedelta(days=to_date)))
        return fire_alarm_objects

    def days_left_in_month():
        today = datetime.date.today()
        _, days_in_month = calendar.monthrange(today.year, today.month)
        days_left = (datetime.date(
            today.year, today.month, days_in_month) - today).days
        return days_left

    def get_context(self) -> Dict[str, any]:
        """
        Returns a dictionary with the Technician object as a value for the key 'technician'.
        """
        context = {'technician': self.technician}
        branch = self.technician.branch
        context['branch'] = branch
        context['branch_location'] = branch.get_location()
        return context


class TechnicianIndex(TechnicianSuit):
    """
    Class that extends TechnicianSuit and adds the 'branch' and 'branch_location' keys to the context dictionary.
    """

    def get_context(self, to_date=None) -> Dict[str, any]:
        """
        Returns a dictionary with the Technician object as a value for the key 'technician', 
        the branch object as a value for the key 'branch', and the branch location as a value for the key 'branch_location'.
        """
        context = super().get_context()
        if to_date is None:
            to_date = 2  # объекты на главной буду которые надо сделать в ближайшие 2 дня
        fire_alarm_objects = self.get_fire_alarm_objects(to_date)
        context['fire_alarm_objects'] = fire_alarm_objects
        context['mobi'] = True  # устанавливает мобильный интерфейс
        context['to_date'] = to_date
        return context


class TechnicianFireAlarmObjects(TechnicianSuit):
    def get_context(self, to_date=None) -> Dict[str, any]:
        """
        Returns a dictionary with the Technician object as a value for the key 'technician', 
        the branch object as a value for the key 'branch', and the branch location as a value for the key 'branch_location'.
        """
        context = super().get_context()
        if to_date is None:
            to_date = 2  # объекты на главной буду которые надо сделать в ближайшие 2 дня
        fire_alarm_objects = self.get_fire_alarm_objects(to_date)
        context['fire_alarm_objects'] = fire_alarm_objects
        context['mobi'] = True  # устанавливает мобильный интерфейс
        context['to_date'] = to_date
        return context


class TechnicianFireAlarmObject(TechnicianSuit):
    def get_context(self, object_id=None) -> Dict[str, any]:
        context = super().get_context()
        fire_alarm_object = get_object_or_404(FireAlarmObject, id=object_id)
        fire_alarm_object_services = FireAlarmObjectService.objects.filter(
            fire_alarm_object_id=object_id).order_by('-service_date')
        failed_services = FailedService.objects.filter(fire_alarm_object_id=object_id).exclude(
            Q(status='completed')).order_by('-service_date')
        context['fire_alarm_object_services']= fire_alarm_object_services
        context['failed_services'] = failed_services
        context['fire_alarm_object'] = fire_alarm_object
        context['fire_alarm_object_geopoint'] = fire_alarm_object.address.get_geopoint()
        context['mobi'] = True  # устанавливает мобильный интерфейс
        return context
