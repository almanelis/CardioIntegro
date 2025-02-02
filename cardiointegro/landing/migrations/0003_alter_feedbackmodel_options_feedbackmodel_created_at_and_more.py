# Generated by Django 5.0.4 on 2024-06-03 16:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_alter_feedbackmodel_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedbackmodel',
            options={'verbose_name': 'Обратная связь', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AddField(
            model_name='feedbackmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedbackmodel',
            name='message',
            field=models.TextField(blank=True, verbose_name='Сообщение'),
        ),
    ]
