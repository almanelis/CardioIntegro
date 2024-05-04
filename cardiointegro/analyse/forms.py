from django import forms

from .models import ECGAnalyse


class ECGAnalyseForm(forms.ModelForm):
    ecg = forms.FileField(label='Файл ЭКГ')
    """Форма создание анализа"""
    class Meta:
        model = ECGAnalyse
        fields = ('title', 'ecg')
