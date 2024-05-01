from django.views.generic import TemplateView


# Класс для вывода главной страницы
class MainPageView(TemplateView):
    template_name = 'main/index.html'
