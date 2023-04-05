from django.shortcuts import render

# Create your views here.
def create_service_zone(request):
    if request.method == 'POST':
        form = ServiceZoneForm(request.POST)
        if form.is_valid():
            service_zone = form.save(commit=False)
            service_zone.geopoints = form.cleaned_data['geopoints']
            service_zone.save()
            # редирект на страницу зоны обслуживания
            return redirect('service_zone_detail', pk=service_zone.pk)
    else:
        form = ServiceZoneForm()
    return render(request, 'create_service_zone.html', {'form': form})