from django import forms
from django.utils.translation import gettext_lazy as _

from .models import FeedbackModel


class FeedbackForm(forms.ModelForm):
    '''Класс формы обратной связи'''
    name = forms.CharField(label='',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Фамилия и имя',
                                      'class': 'block w-full placeholder:text-gray-400 text-gray-50 bg-transparent border-0 border-b-2 border-gray-400 appearance-none focus:outline-none focus:ring-0 focus:border-salad peer'}))
    company = forms.CharField(label='',
                              widget=forms.TextInput(
                               attrs={'placeholder': 'Компания',
                                      'class': 'block w-full placeholder:text-gray-400 text-gray-50 bg-transparent border-0 border-b-2 border-gray-400 appearance-none focus:outline-none focus:ring-0 focus:border-salad peer'}))
    phone_number = forms.CharField(label='',
                                   widget=forms.TextInput(
                                    attrs={'placeholder': 'Номер телефона',
                                           'class': 'block w-full placeholder:text-gray-400 text-gray-50 bg-transparent border-0 border-b-2 border-gray-400 appearance-none focus:outline-none focus:ring-0 focus:border-salad peer'}))
    email = forms.CharField(label='',
                             widget=forms.TextInput(
                               attrs={'placeholder': 'E-mail',
                                      'class': 'block w-full placeholder:text-gray-400 text-gray-50 bg-transparent border-0 border-b-2 border-gray-400 appearance-none focus:outline-none focus:ring-0 focus:border-salad peer'}))
    message = forms.CharField(label='',
                              widget=forms.Textarea(
                               attrs={'placeholder': 'Сообщение',
                                      'class': 'block w-full placeholder:text-gray-400 text-gray-50 bg-transparent border-0 border-b-2 border-gray-400 appearance-none focus:outline-none focus:ring-0 focus:border-salad peer',
                                      'id': 'large-input',
                                      'rows': 2}))
    check_politic = forms.CheckboxInput()
    class Meta:
        model = FeedbackModel
        fields = '__all__'   
