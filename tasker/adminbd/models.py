from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FireSafetyService (models.Model):
    name_object = models.TextField()
    address_object = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_service = models.DateField()
    photo_report = models.ImageField((""), upload_to=None, height_field=None, width_field=None, max_length=None)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

