
def chek_user (APP_RANK):
    """
    1 - Проверяет User автаризован ли он, если нет то перенаправляет на страницу регистрации 
    2 - Проверяет User.rank  на соотвествие APP_RANK, если совпадения не обнаружено, то перенаправляет на сортировку user по его rank
    
    APP_RANK необходимо взять в settings того приложения в котором используется декоратор 
    """
    from django.contrib.auth.decorators import login_required
    def actual_decorator(func):
        from django.shortcuts import redirect
        @login_required
        def wrapper (request, *args, **kwargs):
            if request.user.rank == APP_RANK:
                return  func(request, *args, **kwargs)
            else:
                return redirect('users:sort_users')
        return wrapper
    return actual_decorator