from django.urls import path
from . import views

app_name = 'fitter'

urlpatterns = [
    path('', views.index, name='fitter'),
    path('profile/<username>/', views.profile, name='profile' )
    ]