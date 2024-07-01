from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

from .forms import FeedbackForm


def feedback_view(request):
    '''Функция для обратной связи'''
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        # Проверка валидности и обработка с помощью AJAX
        if form.is_valid() and form.cleaned_data['check_politic']:
            form.save()
            return JsonResponse({'success': True,
                                 'message': 'Спасибо! Ваша форма успешно отправлена'})
        if not form.cleaned_data['check_politic']:
            return JsonResponse({'success': False,
                                 'message': 'Вы должны согласиться с политикой конфиденциальности'})
    else:
        form = FeedbackForm()
    feedback_message = request.session.pop('feedback_message', None)
    context = {'form': form, 'feedback_message': feedback_message}
    return render(request, 'landing/index.html', context)


class KnowledgebaseTemplateView(TemplateView):
    template_name = 'includes/knowledgebase.html'
