from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')


def object_of_protection_list(request):
    return HttpResponse('Список мороженого')


# В урл мы ждем парметр, и нужно его прередать в функцию для использования
def object_of_protection_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')
# Create your views here.
