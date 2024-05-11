from django.views.generic import TemplateView


class MainPageTemplateView(TemplateView):
    template_name = 'landing/landing_page/index.html'


class TutorialTemplateView(TemplateView):
    template_name = 'landing/knowledgebase.html'


class FrontendTemplateView(TemplateView):
    template_name = 'landing/frontend.html'
