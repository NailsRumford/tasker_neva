from django.contrib import admin

from .models import FailedService, FireAlarmObject, FireAlarmObjectService

admin.site.register(FireAlarmObjectService)
admin.site.register(FailedService)
admin.site.register(FireAlarmObject)
