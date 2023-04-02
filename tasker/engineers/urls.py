
from django.urls import path


from . import views

app_name = 'engineers'

urlpatterns = [
    path('', views.index,
         name='index'),
]
