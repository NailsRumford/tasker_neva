def chek_user_rank (APP_RANK):
    def actual_decorator(func):
        from django.shortcuts import redirect
        def wrapper (request, *args, **kwargs):
            if request.user.rank == APP_RANK and request.user.is_authenticated:
                return  func(request, *args, **kwargs)
            else:
                return redirect('users:login')
        return wrapper
    return actual_decorator