from django.urls import path


from . import views

app_name = 'technicians'

urlpatterns = [
    path('', views.index,
         name='index'),
    path('fire_alarm_objects/<int:to_date>/show/', views.fire_alarm_objects, name ='fire_alarm_objects'),
    path('fire_alarm_object_service/<int:object_id>/create/', views.fire_alarm_object_service_create , name='fire_alarm_object_service_create'),
]
