from django.db import models

# Create your models here.
class ServiceOrganizations (models.Model):
    name = models.CharField(verbose_name='Обслуживающая организация',
                            max_length=50,)
    
    class Meta:
        verbose_name = 'Сервесная организация'
        verbose_name_plural = 'Сервисные организации'
        
    def __str__ (self):
        return self.name
    
    