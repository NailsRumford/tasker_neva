from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model

User = get_user_model()



def profile(request, username):
    """Возвращает страничку пользователя с десятью последними постами"""
    user_model = get_object_or_404(User, username=username)
    #user_posts = Post.objects.filter(author__username=username)
    #user_posts_count = Post.objects.filter(author__username=username).count()
    #paginator = Paginator(user_posts, 10)
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)
    template = 'fitter/profile.html'
    context = {'author': user_model}
    #           'user_posts_count': user_posts_count,
    #           'page_obj': page_obj,
    #           }
    return render(request, template, context)


def index(request):
    template = 'fitter/index.html'
    return render(request, template )