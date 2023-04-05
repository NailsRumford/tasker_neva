
from django.urls import path


from . import views

app_name = 'engineers'

urlpatterns = [
    path('', views.index,
         name='index'),
    path('service_zones/', views.service_zones, name = 'service_zones'),
    path('create_service_zone/', views.create_service_zone, name='create_service_zone'),
    path('<int:service_zone_id>/delete/', views.service_zone_delete, name='service_zone_delete'),
    path('<int:service_zone_id>/edit/', views.service_zone_edit, name='service_zone_edit')
]
