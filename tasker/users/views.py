from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from technicians.models import Technician
from engineers.models import Engineer

# def division_users(request):
#
#    context = {'zone':[[55.8177519301427,37.54003187957215],
#                [55.77133254574147,37.71993300261903],
#                [55.710904248186836,37.60869643035341],
#                [55.72563261956205,37.46312758269714],
#                [55.8177519301427,37.54003187957215]]}
#    return render(request, 'index_copy.html', context)
#


def save_polygon(request):
    if request.method == 'POST':
        polygon = request.POST.get('polygon')
    return redirect('home')


@login_required
def division_users(request):
    user = request.user
    if Engineer.objects.filter(user=user).exists():
        success_url = reverse_lazy('tech_dashboard')
    elif Technician.objects.filter(user=user).exists():
        success_url = reverse_lazy('tech_dashboard')
    else:
        success_url = reverse_lazy('users:account_not_confirmed')
    return redirect(success_url)


def account_not_confirmed(request):
    return render(request, 'users/account_not_confirmed.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
