from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')


def object_of_protection_list(request):
    return HttpResponse('Список объектов охраны')


# В урл мы ждем парметр, и нужно его прередать в функцию для использования
def object_of_protection_detail(request, pn):
    return HttpResponse(f'Объект охраны {pn}')
# Create your views here.
