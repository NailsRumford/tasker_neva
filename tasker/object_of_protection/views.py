from django.shortcuts import render


def index(request):
    template = 'object_of_protection\index.html'
    return render(request, template)


def object_of_protection_list(request):
    return render('Список объектов охраны')


# В урл мы ждем парметр, и нужно его прередать в функцию для использования
def object_of_protection_detail(request, pn):
    return render(f'Объект охраны {pn}')
# Create your views here.
