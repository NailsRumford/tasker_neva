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
                  'room_number',
                  'service_organizations',
                  'frequency',
                  'remote_number',
                  'contract_number',
                  'contract_date',
                  'last_service_date',
                  'photo')

    def __init__(self, engineer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['address'] = self.instance.address.address
        self.fields['last_service_date'].widget.attrs['placeholder'] = (
            'дд.мм.гггг')
        self.fields['contract_date'].widget.attrs['placeholder'] = (
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


class FireAlarmObjectServiceForm(forms.ModelForm):
    class Meta:
        model = FireAlarmObjectService
        fields = ('service_journal_title_page_photo','service_journal_photo', 'control_panel_photo', 'comment')


class FailedServiceForm(forms.ModelForm):
    class Meta:
        model = FailedService
        fields = ('photo', 'comment')
