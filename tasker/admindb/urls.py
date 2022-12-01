from django.urls import path, include
from users.views import CreateUser
from . import views

app_name = 'admindb'

urlpatterns = [
    path('create_user/', CreateUser.as_view(), name='create_user' ),
    path('profile/<username>/', views.profile, name='profile' )
] 