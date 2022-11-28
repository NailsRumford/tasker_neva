from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace= 'adminbd')),
    path('auth/', include('django.contrib.auth.urls')),
    path('engineer/', include('engineer.urls', namespace= 'engineer')),
    path('fitter/', include('fitter.urls', namespace= 'fitter')),
    path('researcher/', include('researcher.urls' , namespace= 'researcher')),
    path('repairman/', include('repairman.urls', namespace= 'repairman')),
    path('adminbd/',include('adminbd.urls', namespace= 'adminbd')),
    path('', views.index),
]
