from django.shortcuts import render
from .models import FireSafetyService

def index(request):
    template = 'adminbd\index.html'
    fierSSs = FireSafetyService.objects.filter('-pub_date')[:2]
    contex = { 'fierSSs': fierSSs , }
    return render(request, template, contex )
