from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from technicians.models import Technician
from engineers.models import Engineer
from django.shortcuts import render, redirect


@login_required
def division_users(request):
    user = request.user
    if Engineer.objects.filter(user=user).exists():
        success_url = reverse_lazy('engineers:index')
    elif Technician.objects.filter(user=user).exists():
        success_url = reverse_lazy('tech_dashboard')
    else:
        success_url = reverse_lazy('users:account_not_confirmed')
    return redirect(success_url)


def account_not_confirmed(request):
    return render(request, 'users/account_not_confirmed.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:index')
    template_name = 'users/signup.html'
