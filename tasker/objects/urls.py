from django.contrib.auth import views
from django.urls import path
from .views import address_create

app_name = 'objects'

urlpatterns = [
     
    # Форма адреса
    path('address/', address_create, name='address_create'),

]