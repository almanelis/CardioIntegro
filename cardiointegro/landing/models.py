from django.db import models


class FeedbackModel(models.Model):
    '''Модель обратной связи'''
    name = models.CharField('Фамилия и имя', max_length=128,
                            blank=True, null=True)
    company = models.CharField('Компания', max_length=64,
                               blank=True, null=True)
    phone_number = models.CharField('Номер телефона', max_length=64)
    email = models.CharField('E-mail', max_length=64, blank=True, null=True)
    message = models.TextField('Сообщение', blank=True)
    check_politic = models.BooleanField('', blank=False)
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Сообщения'

    def __str__(self) :
        return f'от {self.name}'
