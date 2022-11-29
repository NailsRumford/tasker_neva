from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

def sort_users(request):
    rank_user = request.user.rank
    if rank_user == 'A':
        return redirect ('admindb:create_user')
    else:
        return redirect ('fitter:fitter')

class CreateUser(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('admindb:create_user')
    template_name = 'users/create_user.html'
    
    
