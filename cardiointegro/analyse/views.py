from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import ECGAnalyse
from .utils import ecg_analyse_process
from .forms import ECGAnalyseForm


@login_required
def analyse_create_view(request):
    """Функция загрузки и анализ ЭКГ"""
    if request.method == 'POST':
        form = ECGAnalyseForm(request.POST, request.FILES)
        # Обработка полученных данных
        if form.is_valid():
            ecg_analyse = form.save(commit=False)
            # Обработка и сохранение графиков анализа
            ecg_file = request.FILES['ecg']
            plot1, plot2, plot3 = ecg_analyse_process(ecg_file)
            ecg_analyse.plot1 = plot1
            ecg_analyse.plot2 = plot2
            ecg_analyse.plot3 = plot3
            # Запись врача, делающего анализ
            ecg_analyse.doctor = request.user
            ecg_analyse.save()
            # Перенаправление на главную страницу
            # return HttpResponseRedirect('analyse/list/')
            target_url = reverse('analyse:detail',
                                 kwargs={'pk': ecg_analyse.id})
            return redirect(target_url)
    else:
        form = ECGAnalyseForm()
    return render(request, 'analyse/analyse_form.html', {'form': form})


@login_required
def analyse_list_view(request):
    user = request.user
    user_analyse = ECGAnalyse.objects.filter(doctor=user).order_by('-created_at')

    # Пагинация
    paginator = Paginator(user_analyse, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    template = 'analyse/analyse_list.html'
    return render(request, template, context)


class AnalyseDetailView(LoginRequiredMixin, DetailView):
    model = ECGAnalyse
    template_name = 'analyse/analyse_detail.html'


@login_required
def analyse_search(request):
    user = request.user
    search_analyse = ECGAnalyse.objects.filter(doctor=user, title__icontains=str(request))
