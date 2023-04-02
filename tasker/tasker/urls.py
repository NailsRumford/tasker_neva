from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from users import views
from django.urls import reverse_lazy
urlpatterns = [
    path('admin/', admin.site.urls),
    ############################################################

    path('login', LoginView.as_view(template_name='users/login.html'),
        name='login'),
    path('signup/', views.SignUp.as_view(template_name='users/signup.html'),
         name='signup'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='users/password_change_form.html'),
        name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='password_change_done'),
    ##########################################################
    path('', include('users.urls', namespace='users')),
    
]

handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'

#if settings.DEBUG:
#    urlpatterns += static(
#        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
#    )
