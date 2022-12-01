from django.urls import path
from . import views

app_name = 'engineer'

urlpatterns = [
    path('', views.index, name='engineer'),
    path('profile/<username>/', views.profile, name='profile' )
] 