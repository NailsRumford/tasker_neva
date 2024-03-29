from django import forms
from .models import ServiceZone, TechnicianZone
from shapely.geometry import Polygon
from django.core.exceptions import ValidationError
from shapely.geometry import Polygon, Point
from fire_alarm_objects.models import FireAlarmObject


def validate_geopoints(value, current_zone_id=None):
    polygon = Polygon(eval(value))
    qs = ServiceZone.objects.exclude(id=current_zone_id)
    for zone in qs:
        if Polygon(eval(zone.geopoints)).intersects(polygon):
            raise ValidationError(f'Имеется пересечение с {zone.name}')


class ServiceZoneForm(forms.ModelForm):
    geopoints = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ServiceZone
        fields = ('name', 'description', 'geopoints')

    def clean_geopoints(self):
        geopoints = self.cleaned_data['geopoints']
        current_zone_id = None
        if self.instance:
            current_zone_id = self.instance.id
        try:
            validate_geopoints(geopoints, current_zone_id)
        except ValidationError as error:
            self.add_error('geopoints', error)
        return geopoints


class AssignZoneToObjectForm (forms.Form):
    service_zone = forms.ModelChoiceField(queryset=None)

    def __init__(self, fire_alarm_object=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if fire_alarm_object is not None:
            zones = ServiceZone.objects.filter(branch=fire_alarm_object.branch)
            self.fields['service_zone'].queryset = zones
    
    def save(self, commit=True):
        zone = self.cleaned_data['service_zone']
        
    

class AssignZonesForm(forms.Form):
    zones = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        label='Выберите зоны для назначения',
    )

    def __init__(self, technician=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получаем зоны, которые не связаны с выбранным техником
        available_zones = ServiceZone.objects.exclude(
            technicians__technician=technician).all()
        self.fields['zones'].queryset = available_zones
        self.technician = technician

    def save(self, commit=True):
        zones = self.cleaned_data['zones']
        technician = self.technician
        if zones:
            for zone in zones:
                technician_zone, status = TechnicianZone.objects.get_or_create(technician=technician,
                                                                               service_zone=zone)
