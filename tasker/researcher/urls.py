from django.urls import path
from . import views

app_name = 'researcher'

urlpatterns = [
    path('', views.index, name='researcher'), 
    ]