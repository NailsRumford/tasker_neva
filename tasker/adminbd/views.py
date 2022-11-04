from django.shortcuts import render


def index(request):
    template = 'adminbd\index.html'
    text = 'Список обслуживания '
    contex = { 'text': text , }
    return render(request, template, contex )
