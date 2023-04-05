from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from engineers.models import Engineer
from technicians.models import Technician


def engineer_required(view_func):
    """
    Декоратор для проверки, является ли текущий пользователь инженером.

    Если текущий пользователь не является инженером или его учетная запись неактивна,
    пользователь будет перенаправлен на страницу входа.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('users:index'))

        try:
            engineer = request.user.engineer
            if not engineer.is_active:
                return redirect(reverse('users:account_not_confirmed'))
        except Engineer.DoesNotExist:
            return redirect(reverse('users:index'))

        return view_func(request, *args, **kwargs)

    return wrapper


def technician_required(view_func):
    """
    Декоратор для проверки, является ли текущий пользователь техником.

    Если текущий пользователь не является техником или его учетная запись неактивна,
    пользователь будет перенаправлен на страницу входа.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('users:index'))

        try:
            technician = request.user.technician
            if not technician.is_active:
                return redirect(reverse('users:account_not_confirmed'))
        except Technician.DoesNotExist:
            return redirect(reverse('users:index'))

        return view_func(request, *args, **kwargs)

    return wrapper