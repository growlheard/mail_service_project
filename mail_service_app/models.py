from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='почта пользователя')
    comments = models.TextField(verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.full_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема письма', default=' ')
    content = models.TextField(verbose_name='Содержание', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.title


class Mailing(models.Model):
    DAILY = 'Ежедневно'
    WEEKLY = 'Еженедельно'
    MONTHLY = 'Ежемесячно'

    FREQUENCY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно')
    ]
    CREATED = 'Создана'
    STARTED = 'Запущена'
    FINISHED = 'Завершена'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена')
    ]

    clients = models.ManyToManyField(Client, verbose_name='Клиенты для рассылки')
    title = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тема письма')
    frequency = models.CharField(max_length=50, verbose_name='Периодичность', choices=FREQUENCY_CHOICES, default=DAILY)
    mailing_status = models.CharField(max_length=50, verbose_name='Статус рассылки', choices=STATUS_CHOICES,
                                      default=CREATED)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    SENT = 'Отправлено'
    FAILED = 'Не удалось отправить'
    PENDING = 'В ожидании'

    STATUS_CHOICES = [
        (SENT, 'Отправлено'),
        (FAILED, 'Не удалось отправить'),
        (PENDING, 'В ожидании')
    ]

    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    status = models.CharField(max_length=20, verbose_name='Статус')
    error_message = models.TextField(blank=True, null=True, verbose_name='Ошибка')

    class Meta:
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылок'
