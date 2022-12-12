from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('engineer/', include('engineer.urls', namespace='engineer')),
    path('admindb/', include('admindb.urls', namespace='admindb')),
    path('fitter/', include('fitter.urls', namespace='fitter')),
    path('researcher/', include('researcher.urls', namespace='researcher')),
    path('repairman/', include('repairman.urls', namespace='repairman')),
    path('objects/', include('objects.urls', namespace='objects')),
    path('', include('users.urls', namespace='users')),
]
