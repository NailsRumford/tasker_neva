from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm


class CreateUser(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('admindb:create_user')
    template_name = 'users/create_user.html'