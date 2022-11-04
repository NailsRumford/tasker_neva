from django.urls import path
from . import views

app_name = 'adminbd'


urlpatterns = [
    path('', views.index, name= 'adminbd'),
] 