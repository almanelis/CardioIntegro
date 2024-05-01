from django.http import HttpResponse
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main/index.html'