from django.urls import path, include
from users.views import CreateUser

app_name = 'admindb'

urlpatterns = [
    path('create_user/', CreateUser.as_view(), name='create_user' ),
] 