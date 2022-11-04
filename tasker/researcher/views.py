from django.shortcuts import render


def index(request):
    template = 'researcher/index.html'
    return render(request, template )