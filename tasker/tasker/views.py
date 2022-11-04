from django.shortcuts import render


def index(request):
    template = 'tasker/index.html'
    return render(request, template )