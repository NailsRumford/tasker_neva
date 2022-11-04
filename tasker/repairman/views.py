from django.shortcuts import render


def index(request):
    template = 'repairman/index.html'
    return render(request, template )