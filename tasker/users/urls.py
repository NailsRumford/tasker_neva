from django.contrib.auth import views
from django.urls import path
from .views import sort_users, Test

app_name = 'users'

urlpatterns = [
    # Авторизация
    path('', views.LoginView.as_view(template_name='users/index.html'), name='login'),
    # Выход
    path('auth/logout/', views.LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    # Смена пароля
    path('auth/password_change/', Test.as_view(template_name='users/password_change_form.html'),
         name='password_change'),
    # Сообщение об успешном изменении пароля
    path('auth/password_change/done/', views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # Восстановление пароля
    path('auth/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля
    path('auth/password_reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # Вход по ссылке для восстановления пароля
    path('auth/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля
    path('auth/reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
