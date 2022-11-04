from django.shortcuts import render


def index(request):
    template = 'engineer/index.html'
    return render(request, template )