from django import forms
from .models import FireAlarmObject, FireAlarmObjectService, FailedService
from dadata import Dadata
from .models import Address
from tasker.settings import DADATA_SECRET, DADATA_TOKEN
from service_zones.models import ServiceZone

class FireAlarmObjectForm(forms.ModelForm):
    address = forms.CharField(required=True,
                              max_length=200,
                              label='Адресс',
                              help_text='Введите адресс',)
    latitude = forms.CharField(required=False,
                               max_length=200,
                               label='Широта',
                               help_text='Введите широту',)
    longitude = forms.CharField(required=False,
                                max_length=200,
                                label='Долгота',
                                help_text='Введите долготу',)

    class Meta:
        model = FireAlarmObject
        fields = ('name',
                  'latitude',
                  'longitude',
                  'address',
                  'service_organizations',
                  'frequency',
                  'last_service_date',
                  'photo')

    def __init__(self, engineer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_service_date'].widget.attrs['placeholder'] = (
            'дд.мм.гггг')

    def clean_address(self):
        address = self.cleaned_data.get('address')
        dadata = Dadata(token=DADATA_TOKEN, secret=DADATA_SECRET)
        result = dadata.clean("address", address)
        verification_status = result['qc']
        if verification_status != 0:
            if self.cleaned_data.get('latitude') and self.cleaned_data.get('longitude'):
                address_object, status = Address.objects.get_or_create(
                    address=address,
                    latitude=self.cleaned_data.get('latitude'),
                    longitude=self.cleaned_data.get('longitude'))
                return address_object
            raise forms.ValidationError(
                'Адрес не распознан. Добавте координады для добавления объекта.')
        address = result['result']
        latitude = result['geo_lat']
        longitude = result['geo_lon']
        address_object, status = Address.objects.get_or_create(
            address=address,
            latitude=latitude,
            longitude=longitude)
        return address_object

class AddZone2FireAlarmObjectForm(forms.ModelForm):
    service_zone = forms.ChoiceField(
        choices=[],
        label='Филиал')
    class Meta:
        model = FireAlarmObject
        fields = ('service_zone',)

    def __init__(self, engineer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_zone'].choices = [(service_zone.pk, service_zone.name) for service_zone in self.service_zones]

        self.service_zones = ServiceZone.objects.filter(branch=engineer.branch)



class FireAlarmObjectServiceForm(forms.ModelForm):
    class Meta:
        model = FireAlarmObjectService
        fields = ('service_journal_photo', 'control_panel_photo', 'comment')


class FailedServiceForm(forms.ModelForm):
    class Meta:
        model = FailedService
        fields = ('photo', 'comment')
