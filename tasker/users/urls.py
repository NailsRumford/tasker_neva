from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path
from django.urls import reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('save_polygon/', views.save_polygon, name='save_polygon'),
    path('account_not_confirmed/', views.account_not_confirmed,
         name='account_not_confirmed'),
    path('', views.division_users,
         name='index'),
]
