from django.shortcuts import redirect, render

from . import forms
from . import models


def address_create(request):
    template = 'objects/create_address.html'
    form = forms.AddressSOForm(request.POST or None)
    if form.is_valid():
        сountryModel = models.CountrySOModel.objects.get_or_create(
            name=form.cleaned_data['сountry'])
        regionModel = models.RegionSOModel.objects.get_or_create(
            country=сountryModel,
            name=form.cleaned_data['region'])
        cityModel = models.CitySOModel.objects.get_or_create(
            country=сountryModel,
            region=regionModel,
            name=form.cleaned_data['city'])
        streetModel = models.StreetSOModel.objects.get_or_create(
            country= сountryModel,
            region = regionModel,
            city = cityModel,
            name = form.cleaned_data['street'])
        buildingModel = models.BuildingSOModel.objects.get_or_create(
            country = сountryModel,
            region = regionModel,
            city = cityModel,
            street = streetModel,
            number = form.cleaned_data['building'],
            liter = form.cleaned_data['building_liter'] or None)
        roomModel = models.RoomSOModel.objects.get_or_create(
            country = сountryModel,
            region = regionModel,
            city = cityModel,
            street = streetModel,
            building = buildingModel,
            number = form.cleaned_data['room'],
            liter = form.cleaned_data['room_litter'] or None
        )

        print(a)
        return redirect('users:login')
    return render(request, template, {'form': form})


# def address_create(request):
#    """ Возвращает форму для добавления новой публикации """
#    template = 'objects/create_address.html'
#
#    country_form= forms.CountrySOForm(request.POST or None)
#    region_form = forms.RegionSOForm(request.POST or None)
#    city_form = forms.CitySOForm(request.POST or None)
#    street_form = forms.StreetSOForm(request.POST or None)
#    building_form = forms.BuildingSOForm(request.POST or None)
#    room_form = forms.RoomSOFrom(request.POST or None)
#    if (country_form.is_valid()
#        and region_form.is_valid()
#        and city_form.is_valid()
#        and street_form.is_valid()
#        and building_form.is_valid()
#        and room_form.is_valid()):
#
#
#
#        region = region_form.save(commit=False)
#        country = country_form.save()
#        region.country = country
#        region.save()
#        return redirect('users:login')
#    return render(request, template, {'form': country_form,
#                                      'form2': region_form})
