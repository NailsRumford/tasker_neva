from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import Engineer, Tech
from .forms import CreationForm
from django.shortcuts import render,redirect


def division_users(request):
    #user = request.user
    #if Engineer.objects.filter(user=user).exists():
    #    success_url = reverse_lazy('tech_dashboard')
    #elif Tech.objects.filter(user=user).exists():
    #    success_url = reverse_lazy('tech_dashboard')
    #else:
    #    success_url = reverse_lazy('dashboard')
    return redirect()
    


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'