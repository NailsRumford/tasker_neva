from django import forms
from .models import ServiceZone
from shapely.geometry import Polygon
from django.core.exceptions import ValidationError
from functools import  partial


def validate_geopoints(value, current_zone_id=None):
    polygon = Polygon(eval(value))
    qs = ServiceZone.objects.exclude(id=current_zone_id)
    for zone in qs:
        if Polygon(eval(zone.geopoints)).intersects(polygon):
            raise ValidationError(f'Имеется пересечение с {zone.name}')
      
class ServiceZoneForm(forms.ModelForm):
    geopoints = forms.CharField(widget=forms.HiddenInput())

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

    class Meta:
        model = ServiceZone
        fields = ('name', 'description', 'geopoints')