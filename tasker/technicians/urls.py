from django.urls import path


from . import views

app_name = 'technicians'

urlpatterns = [
    path('', views.index,
         name='index'),
    path('fire_alarm_objects/<int:to_date>/show/', views.fire_alarm_objects, name ='fire_alarm_objects'),
    path('make_service/<int:object_id>/create/', views.make_service , name='make_service'),
]
