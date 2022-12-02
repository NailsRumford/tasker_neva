from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .settings import RANK_APP


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
    
