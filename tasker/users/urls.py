
from django.urls import path


from . import views

app_name = 'users'

urlpatterns = [
    path('account_not_confirmed/', views.account_not_confirmed,
         name='account_not_confirmed'),
    path('', views.division_users,
         name='index'),
]
