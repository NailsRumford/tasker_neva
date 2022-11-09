from django.contrib import admin
from .models import FireSafetyService


class FireSafetySrviceAdmin (admin.ModelAdmin):
    list_display = ['name_object', 'address_object', 'pub_date', 'last_service', 'author',]

admin.site.register(FireSafetyService, FireSafetySrviceAdmin)
# Register your models here.
