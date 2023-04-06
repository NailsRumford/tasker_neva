
from django.urls import path


from . import views

app_name = 'engineers'

urlpatterns = [
    path('', views.index,
         name='index'),
    path('service_zones/', views.service_zones, name='service_zones'),
    path('create_service_zone/', views.create_service_zone,
         name='create_service_zone'),
    path('service_zone/<int:service_zone_id>/delete/',
         views.service_zone_delete, name='service_zone_delete'),
    path('service_zone/<int:service_zone_id>/edit/',
         views.service_zone_edit, name='service_zone_edit'),
    path('technicians/', views.technicians, name='technicians'),
    path('technician/<int:technician_id>/detail/',
         views.technician_detail, name='technician_detail'),
    path('technician/<int:technician_id>/activate/',
         views.technician_activate, name='technician_activate'),
    path('technician/<int:technician_id>/deactivate/',
         views.technician_deactivate, name='technician_deactivate'),
    path('technician_zone/<int:technician_zone_id>/delete/',
         views.technician_zone_delete, name='technician_zone_delete'),
    path('fire_alarm_objects/', views.fire_alarm_objects,
         name='fire_alarm_objects'),
    path('create_fire_alarm_object', views.create_fire_alarm_object,
         name='create_fire_alarm_object')
]
