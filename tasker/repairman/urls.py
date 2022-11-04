from django.urls import path
from . import views

app_name = 'repairman'

urlpatterns = [
    path('', views.index, name='repairman'), ]