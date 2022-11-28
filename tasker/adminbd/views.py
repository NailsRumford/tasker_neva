from django.shortcuts import render
import django.contrib.auth
from .models import FireSafetyService

def index(request):
    template = 'adminbd\index.html'
    fireSSs =  FireSafetyService.objects.order_by('-pub_date')[:2]
    contex = { 'fireSSs': fireSSs , }
    return render(request, template, contex )
