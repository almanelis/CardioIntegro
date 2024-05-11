from django import forms

from .models import ECGAnalyse


class CustomFileWidget(forms.FileInput):
    pass


class ECGAnalyseForm(forms.ModelForm):
    ecg = forms.FileField(widget=CustomFileWidget(
        attrs={"class": "rounded-lg border w-full", }
        ),
        label='Файл ЭКГ',
        )
    """Форма создание анализа"""
    class Meta:
        model = ECGAnalyse
        fields = ('title', 'ecg')
