from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class UserCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse('/')
