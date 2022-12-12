from django import forms
from . import models

class AddressSOForm (forms.Form):
    сountry = forms.CharField(max_length=50 )
    region = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50) 
    street = forms.CharField(max_length=100)
    building = forms.CharField(max_length=10)
    building_liter = forms.CharField(max_length=10)
    room = forms.CharField(max_length=5)
    room_liter = forms.CharField(max_length=10)
        
class CountrySOForm (forms.ModelForm):
    class Meta:
        model = models.CountrySOModel
        fields = ('country_name',)
        auto_id='id_for_country_%s'

class RegionSOForm(forms.ModelForm):
    class Meta:
        model = models.RegionSOModel
        fields = ('region_name',)
        auto_id='id_for_region_%s'
        
class  CitySOForm(forms.ModelForm):
    class Meta:
        model = models.CitySOModel
        fields = ('name',)
        auto_id='id_for_city_%s'
        
class StreetSOForm(forms.ModelForm):
    class Meta:
        model = models.StreetSOModel
        fields = ('name',)
        auto_id='id_for_street_%s'
        
        
class BuildingSOForm(forms.ModelForm):
    class Meta:
        model = models.BuildingSOModel
        fields = ('number', 'liter',)
        auto_id='id_for_building_%s' 

class RoomSOFrom(forms.ModelForm):
    class Meta:
        model = models.RoomSOModel
        fields = ('number', 'liter',)
        auto_id='id_for_room_%s' 
