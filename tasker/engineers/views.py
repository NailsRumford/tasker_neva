from django.shortcuts import render

def index(request):
    template = 'engineers/index.html'
    return render(request, template_name=template)