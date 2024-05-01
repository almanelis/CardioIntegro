from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegisterForm


# Фукция входа пользователя(django>=3.0)
def logout_view(request):
    logout(request)
    return redirect('/')


# Класс создания нового пользователя
class CreateUserView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
