from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .settings import RANK_APP
from django.contrib.auth import views

@login_required
def sort_users(request):
    user_rank = request.user.rank
    username = request.user.username
    if user_rank in RANK_APP:
        return redirect (RANK_APP[user_rank],username)
    else:
        return redirect ('users:login')


class CreateUser(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('admindb:create_user')
    template_name = 'users/create_user.html'
    
class Test(views.PasswordChangeView):
    template_name ='users/password_change_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        testt = self.request.user.rank + '/base.html'
        context.update(
        {"testt":testt , "title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context   
    