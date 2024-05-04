# Generated by Django 5.0.4 on 2024-05-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ECGAnalyse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='ФИО пациента')),
                ('ecg', models.FileField(blank=True, null=True, upload_to='ecg/', verbose_name='Файл ЭКГ')),
                ('plot1', models.ImageField(upload_to='', verbose_name='Анализ 1')),
                ('plot2', models.ImageField(upload_to='', verbose_name='Анализ 2')),
                ('plot3', models.ImageField(upload_to='', verbose_name='Анализ 3')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
        ),
    ]
