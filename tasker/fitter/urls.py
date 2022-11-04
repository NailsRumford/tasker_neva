from django.urls import path
from . import views

app_name = 'fitter'

urlpatterns = [
    path('', views.index, name='fitter'), ]