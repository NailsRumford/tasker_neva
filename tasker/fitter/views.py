from django.shortcuts import render


def index(request):
    template = 'fitter/index.html'
    return render(request, template )