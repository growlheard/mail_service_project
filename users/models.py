from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db import models
from mail_service_app.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='статус активации')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32)
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'set_is_active',
                'Can block user'
            ),
        ]
