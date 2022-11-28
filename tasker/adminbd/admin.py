from django.contrib import admin
from .models import FireSafetyService


class FireSafetySrviceAdmin (admin.ModelAdmin):
    list_display = ['name_object', 'address_object', 'pub_date', 'last_service', 'author',]
    list_editable = ('last_service',)
    empty_value_display = '-пусто-'
    
admin.site.register(FireSafetyService, FireSafetySrviceAdmin)



# Register your models here.
