from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# upload_analyse_file_path(instance)


class ECGAnalyse(models.Model):
    """Модель анализа"""
    title = models.CharField('ФИО пациента', max_length=200)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Медицинский работник')
    ecg = models.FileField('Файл ЭКГ', upload_to='ecg/',
                           blank=True, null=True)
    plot1 = models.ImageField('Анализ 1')
    plot2 = models.ImageField('Анализ 2')
    plot3 = models.ImageField('Анализ 3')

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('main:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
