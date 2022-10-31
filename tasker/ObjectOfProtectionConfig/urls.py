from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('object_of_protection/', views.object_of_protection_list),
    path('object_of_protection/<int:pn>/', views.object_of_protection_detail),
] 